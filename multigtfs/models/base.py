#
# Copyright 2012 John Whitlock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from csv import DictReader, writer
from datetime import datetime, date
from StringIO import StringIO

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.fields.related import ManyToManyField


class BaseQuerySet(QuerySet):
    def export_txt(self):
        '''Export records as a GTFS comma-separated file'''
        # If no records, return None
        if not self.exists():
            return
        csv_names = []
        for csv_name, field_pattern in self.model._column_map:
            # Separate the local field name from foreign columns
            if '__' in field_pattern:
                field_name, rel_name = field_pattern.split('__', 1)
            else:
                field_name, rel_name = (field_pattern, None)
            # Only add optional columns if they are used in the records
            field = self.model._meta.get_field_by_name(field_name)[0]
            if field.blank and not field.has_default():
                if field.null:
                    blank = None
                else:
                    blank = field.value_to_string(None)
                kwargs = {field_name: blank}
                if self.exclude(**kwargs).exists():
                    csv_names.append((csv_name, field_pattern))
            else:
                csv_names.append((csv_name, field_pattern))
        # Create and return the CSV
        return self.create_csv(csv_names)

    def create_csv(self, csv_names):
        """Turn a queryset into a CSV export

        Keyword Arguments:
        queryset -- A queryset with at least one record
        csv_names -- A sequnce of (csv column, field name) pairs

        A field name can follow relations, such as 'field1__subfield2'
        """
        columns, fields = zip(*csv_names)

        # Avoid ordering by ManyToManyFields, which result in duplicate objects
        if hasattr(self.model, '_sort_order'):
            sort_fields = self.model._sort_order
        else:
            sort_fields = []
            for field in fields:
                base_field = field.split('__', 1)[0]
                field_type = self.model._meta.get_field_by_name(base_field)[0]
                if not isinstance(field_type, ManyToManyField):
                    sort_fields.append(field)

        rows = [columns]
        for item in self.order_by(*sort_fields):
            row = []
            many_pos = None
            for csv_name, field_name in csv_names:
                obj = item
                while obj and '__' in field_name:
                    parent_field, field_name = field_name.split('__', 1)
                    obj = getattr(obj, parent_field)
                if hasattr(obj, 'all'):
                    assert many_pos is None
                    many_pos = len(row)
                    many = [str(getattr(o, field_name)) for o in obj.all()]
                    row.append(many)
                else:
                    field = getattr(obj, field_name) if obj else ''
                    if isinstance(field, date):
                        row.append(field.strftime('%Y%m%d'))
                    elif isinstance(field, bool):
                        row.append(1 if field else 0)
                    elif field is None:
                        row.append('')
                    else:
                        row.append(unicode(field).encode('utf-8'))
            if many_pos:
                many = row[many_pos]
                for m in sorted(many):
                    new_row = row[:]
                    new_row[many_pos] = m
                    rows.append(new_row)
            else:
                rows.append(row)
        out = StringIO()
        writer(out, lineterminator='\n').writerows(rows)
        return out.getvalue()


class BaseManager(models.Manager):

    def get_query_set(self):
        return BaseQuerySet(self.model)

    def in_feed(self, feed):
        '''Return the objects in the target feed'''
        kwargs = {self.model._rel_to_feed: feed}
        return self.filter(**kwargs)


class Base(models.Model):
    """Base class for models that are defined in the GTFS spec

    Implementers need to define a class variable:

    _column_map - A mapping of GTFS columns to model fields
    It should be set to a sequence of tuples:
    - GTFS column name
    - Model field name

    If the column is optional, then set blank=True on the field, and set
    null=True appropriately.

    Implementers can define this class variable:

    _rel_to_feed - The relation of this model to the field, in Django filter
    format.  The default is 'feed', and will be used to get the objects
    on a feed like this:
    Model.objects.filter(_rel_to_feed=feed)

    """

    class Meta:
        abstract = True
        app_label = 'multigtfs'

    objects = BaseManager()

    # The relation of the model to the feed it belongs to.
    _rel_to_feed = 'feed'

    @classmethod
    def import_txt(cls, txt_file, feed):
        '''Import from the GTFS text file'''

        # Setup the conversion from GTFS to Django Format
        # Conversion functions
        no_convert = lambda value: value
        date_convert = lambda value: datetime.strptime(value, '%Y%m%d')
        bool_convert = lambda value: value == '1'
        char_convert = lambda value: value or ''
        null_convert = lambda value: value or None

        def default_convert(field):
            def get_value_or_default(value):
                if value == '' or value is None:
                    return field.get_default()
                else:
                    return value
            return get_value_or_default

        def instance_convert(field, feed, rel_name):
            def get_instance(value):
                if value:
                    kwargs = {field.rel.to._rel_to_feed: feed, rel_name: value}
                    return field.rel.to.objects.get_or_create(**kwargs)[0]
                else:
                    return None
            return get_instance

        # Map of field_name to converters from GTFS to Django format
        val_map = dict()
        m2m_map = dict()
        name_map = dict()
        for csv_name, field_pattern in cls._column_map:
            # Separate the local field name from foreign columns
            if '__' in field_pattern:
                field_name, rel_name = field_pattern.split('__', 1)
            else:
                field_name, rel_name = (field_pattern, None)
            # Use the field name in the name mapping
            name_map[csv_name] = field_name

            # Pick a conversion function for the field
            field = cls._meta.get_field_by_name(field_name)[0]
            is_m2m = False
            if isinstance(field, models.DateField):
                converter = date_convert
            elif isinstance(field, models.BooleanField):
                converter = bool_convert
            elif isinstance(field, models.CharField):
                converter = char_convert
            elif field.rel:
                converter = instance_convert(field, feed, rel_name)
                is_m2m = isinstance(field, models.ManyToManyField)
            elif field.null:
                converter = null_convert
            elif field.has_default():
                converter = default_convert(field)
            else:
                converter = no_convert

            if is_m2m:
                m2m_map[csv_name] = converter
            else:
                val_map[csv_name] = converter

        # Read and convert the source txt
        reader = DictReader(txt_file)
        for row in reader:
            fields = dict()
            m2ms = dict()
            if cls._rel_to_feed == 'feed':
                fields['feed'] = feed
            for column_name, value in row.items():
                if not column_name in name_map:
                    if value:
                        raise ValueError(
                            'Unexpected column name %s in row %s, expecting'
                            ' %s' % (column_name, row, name_map.keys()))
                elif column_name in val_map:
                    fields[name_map[column_name]] = val_map[column_name](value)
                else:
                    assert column_name in m2m_map
                    m2ms[name_map[column_name]] = m2m_map[column_name](value)
            if m2ms:
                obj, created = cls.objects.get_or_create(**fields)
                for field_name, value in m2ms.items():
                    getattr(obj, field_name).add(value)
            else:
                cls.objects.create(**fields)
