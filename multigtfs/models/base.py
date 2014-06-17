#
# Copyright 2012-2014 John Whitlock
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
from __future__ import unicode_literals
from csv import DictReader, writer
from datetime import datetime, date
from logging import getLogger
import re

from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.db.models.fields.related import ManyToManyField
from django.utils.six import StringIO, text_type

logger = getLogger(__name__)
re_point = re.compile(r'(?P<name>point)\[(?P<index>\d)\]')


class BaseQuerySet(GeoQuerySet):
    def export_txt(self):
        '''Export records as a GTFS comma-separated file'''
        # If no records, return None
        if not self.exists():
            return
        csv_names = []
        for csv_name, field_pattern in self.model._column_map:
            # Separate the local field name from foreign columns
            if '__' in field_pattern:
                field_name = field_pattern.split('__', 1)[0]
            else:
                field_name = field_pattern

            # Handle point fields
            point_match = re_point.match(field_name)
            if point_match:
                field = None
            else:
                field = self.model._meta.get_field_by_name(field_name)[0]

            # Only add optional columns if they are used in the records
            if field and field.blank and not field.has_default():
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
        csv_names -- A sequence of (csv column, field name) pairs

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
                point_match = re_point.match(base_field)
                if point_match:
                    continue
                field_type = self.model._meta.get_field_by_name(base_field)[0]
                assert not isinstance(field_type, ManyToManyField)
                sort_fields.append(field)

        rows = [[text_type(c) for c in columns]]
        for item in self.order_by(*sort_fields):
            row = []
            for csv_name, field_name in csv_names:
                obj = item
                while obj and '__' in field_name:
                    parent_field, field_name = field_name.split('__', 1)
                    obj = getattr(obj, parent_field)
                point_match = re_point.match(field_name)
                assert not hasattr(obj, 'all')
                if point_match:
                    name, index = point_match.groups()
                    field = getattr(obj, name)
                    row.append(field.coords[int(index)])
                else:
                    field = getattr(obj, field_name) if obj else ''
                    if isinstance(field, date):
                        formatted = field.strftime(u'%Y%m%d')
                        row.append(text_type(formatted))
                    elif isinstance(field, bool):
                        row.append(1 if field else 0)
                    elif field is None:
                        row.append(u'')
                    else:
                        row.append(text_type(field))
            rows.append(row)

        out = StringIO()
        csv_writer = writer(out, lineterminator='\n')
        for row in rows:
            try:
                csv_writer.writerow(row)
            except UnicodeEncodeError:  # pragma: no cover
                # Python 2 csv does badly with unicode outside of ASCII
                new_row = []
                for item in row:
                    if isinstance(item, text_type):
                        new_row.append(item.encode('utf-8'))
                    else:
                        new_row.append(item)
                csv_writer.writerow(new_row)
        return out.getvalue()


class BaseManager(models.GeoManager):

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
        point_convert = lambda value: value or 0.0

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

        # Check unique fields
        column_names = [c for c, _ in cls._column_map]
        for unique_field in cls._unique_fields:
            assert unique_field in column_names, \
                '{} not in {}'.format(unique_field, column_names)

        # Map of field_name to converters from GTFS to Django format
        val_map = dict()
        name_map = dict()
        point_map = dict()
        for csv_name, field_pattern in cls._column_map:
            # Separate the local field name from foreign columns
            if '__' in field_pattern:
                field_name, rel_name = field_pattern.split('__', 1)
            else:
                field_name, rel_name = (field_pattern, None)
            # Use the field name in the name mapping
            name_map[csv_name] = field_name

            # Is it a point field?
            point_match = re_point.match(field_name)
            if point_match:
                field = None
            else:
                field = cls._meta.get_field_by_name(field_name)[0]

            # Pick a conversion function for the field
            if point_match:
                converter = point_convert
            elif isinstance(field, models.DateField):
                converter = date_convert
            elif isinstance(field, models.BooleanField):
                converter = bool_convert
            elif isinstance(field, models.CharField):
                converter = char_convert
            elif field.rel:
                converter = instance_convert(field, feed, rel_name)
                assert not isinstance(field, models.ManyToManyField)
            elif field.null:
                converter = null_convert
            elif field.has_default():
                converter = default_convert(field)
            else:
                converter = no_convert

            if point_match:
                index = int(point_match.group('index'))
                point_map[csv_name] = (index, converter)
            else:
                val_map[csv_name] = converter

        # Read and convert the source txt
        reader = DictReader(txt_file)
        unique_line = dict()
        for row in reader:
            fields = dict()
            point_coords = [None, None]
            ukey_values = {}
            if cls._rel_to_feed == 'feed':
                fields['feed'] = feed
            for column_name, value in row.items():
                if column_name not in name_map:
                    if value:
                        raise ValueError(
                            'Unexpected column name %s in row %s, expecting'
                            ' %s' % (column_name, row, name_map.keys()))
                elif column_name in val_map:
                    fields[name_map[column_name]] = val_map[column_name](value)
                else:
                    assert column_name in point_map
                    pos, converter = point_map[column_name]
                    point_coords[pos] = converter(value)

                # Is it part of the unique key?
                if column_name in cls._unique_fields:
                    ukey_values[column_name] = value

            # Join the lat/long into a point
            if point_map:
                assert point_coords[0] and point_coords[1]
                fields['point'] = "POINT(%s)" % (' '.join(point_coords))

            # Is the item unique?
            ukey = tuple(ukey_values.get(u) for u in cls._unique_fields)
            if ukey in unique_line:
                logger.warning(
                    '%s line %d is a duplicate of line %d, not imported.',
                    cls._filename, reader.line_num, unique_line[ukey])
                continue
            else:
                unique_line[ukey] = reader.line_num

            # Create the item
            cls.objects.create(**fields)
