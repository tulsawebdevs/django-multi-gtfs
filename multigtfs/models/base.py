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
from collections import defaultdict
from csv import DictReader, writer
from datetime import datetime, date
from logging import getLogger
import re

from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.db.models.fields.related import ManyToManyField
from django.utils.six import StringIO, text_type
from jsonfield import JSONField

logger = getLogger(__name__)
re_point = re.compile(r'(?P<name>point)\[(?P<index>\d)\]')
batch_size = 1000


class BaseQuerySet(GeoQuerySet):
    def populated_column_map(self):
        '''Return the _column_map without unused optional fields'''
        column_map = []
        cls = self.model
        for csv_name, field_pattern in cls._column_map:
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
                field = cls._meta.get_field_by_name(field_name)[0]

            # Only add optional columns if they are used in the records
            if field and field.blank and not field.has_default():
                if field.null:
                    blank = None
                else:
                    blank = field.value_to_string(None)
                kwargs = {field_name: blank}
                if self.exclude(**kwargs).exists():
                    column_map.append((csv_name, field_pattern))
            else:
                column_map.append((csv_name, field_pattern))
        return column_map


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

    extra_data = JSONField(default={})

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
        cache = {}

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
                    key1 = "{}:{}".format(field.rel.to.__name__, rel_name)
                    key2 = text_type(value)

                    # Load existing objects
                    if key1 not in cache:
                        pairs = field.rel.to.objects.filter(
                            **{field.rel.to._rel_to_feed: feed}).values_list(
                            rel_name, 'id')
                        cache[key1] = dict((text_type(x), i) for x, i in pairs)

                    # Create new?
                    if key2 not in cache[key1]:
                        kwargs = {
                            field.rel.to._rel_to_feed: feed,
                            rel_name: value}
                        cache[key1][key2] = field.rel.to.objects.create(
                            **kwargs).id
                    return cache[key1][key2]
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
                field_base, rel_name = field_pattern.split('__', 1)
                field_name = field_base + '_id'
            else:
                field_name = field_base = field_pattern
            # Use the field name in the name mapping
            name_map[csv_name] = field_name

            # Is it a point field?
            point_match = re_point.match(field_name)
            if point_match:
                field = None
            else:
                field = cls._meta.get_field_by_name(field_base)[0]

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
        count = 0
        extra_counts = defaultdict(int)
        new_objects = []
        for row in reader:
            fields = dict()
            point_coords = [None, None]
            ukey_values = {}
            if cls._rel_to_feed == 'feed':
                fields['feed'] = feed
            for column_name, value in row.items():
                if column_name not in name_map:
                    val = null_convert(value)
                    if val is not None:
                        fields.setdefault('extra_data', {})[column_name] = val
                        extra_counts[column_name] += 1
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

            # Create after accumulating a batch
            new_objects.append(cls(**fields))
            if len(new_objects) % batch_size == 0:  # pragma: no cover
                cls.objects.bulk_create(new_objects)
                count += len(new_objects)
                logger.info(
                    "Imported %d %s",
                    count, cls._meta.verbose_name_plural)
                new_objects = []

        # Create remaining objects
        if new_objects:
            cls.objects.bulk_create(new_objects)

        # Take note of extra fields
        if extra_counts:
            extra_columns = feed.meta.setdefault(
                'extra_columns', {}).setdefault(cls.__name__, [])
            for column in extra_counts:
                if column not in extra_columns:
                    extra_columns.append(column)
            feed.save()
        return len(unique_line)

    @classmethod
    def export_txt(cls, feed):
        '''Export records as a GTFS comma-separated file'''
        objects = cls.objects.in_feed(feed)

        # If no records, return None
        if not objects.exists():
            return

        column_map = objects.populated_column_map()
        columns, fields = zip(*column_map)
        extra_columns = feed.meta.get(
            'extra_columns', {}).get(cls.__name__, [])

        # Avoid ordering by ManyToManyFields, which result in duplicate objects
        if hasattr(objects.model, '_sort_order'):
            sort_fields = objects.model._sort_order
        else:
            sort_fields = []
            for field in fields:
                base_field = field.split('__', 1)[0]
                point_match = re_point.match(base_field)
                if point_match:
                    continue
                field_type = objects.model._meta.get_field_by_name(
                    base_field)[0]
                assert not isinstance(field_type, ManyToManyField)
                sort_fields.append(field)
        header_row = [text_type(c) for c in columns]
        header_row.extend(extra_columns)
        rows = [header_row]
        out = StringIO()
        csv_writer = writer(out, lineterminator='\n')
        count = 0
        cache = {}
        feed = None

        def write_rows():
            '''Write a batch of row data to the csv'''
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

        total = objects.count()
        logger.info(
            '%d %s to export...',
            total, objects.model._meta.verbose_name_plural)

        # For large querysets, break it up
        if total < 100000:
            querysets = [objects.order_by(*sort_fields)]
        else:  # pragma: no cover
            field1_raw = sort_fields[0]
            assert '__' in field1_raw
            field1 = field1_raw.split('__', 1)[0]
            field1_id = field1 + '_id'
            querysets = []
            unique = objects.order_by(
                field1_raw).values_list(field1_id, flat=True).distinct()
            for field1_val in unique:
                qs = objects.filter(
                    **{field1: field1_val}).order_by(*sort_fields[1:])
                querysets.append(qs)

        for queryset in querysets:
            for item in queryset.order_by(*sort_fields):
                row = []
                for csv_name, field_name in column_map:
                    obj = item
                    point_match = re_point.match(field_name)
                    if '__' in field_name:
                        # Return relations from cache
                        local_field_name, subfield_name = field_name.split(
                            '__', 1)
                        field_id = getattr(obj, local_field_name + '_id')
                        if field_name not in cache:
                            # Get the feed
                            if feed is None:
                                feed_path = objects.model._rel_to_feed
                                feed_obj = obj
                                while '__' in feed_path:
                                    feed_field, feed_path = feed_path.split(
                                        '__', 1)
                                    feed_obj = getattr(feed_obj, feed_field)
                                feed = getattr(feed_obj, feed_path)

                            # Get all the objects
                            field = obj._meta.get_field_by_name(
                                local_field_name)[0]
                            field_type = field.rel.to
                            pairs = field_type.objects.filter(
                                **{field_type._rel_to_feed: feed}).values_list(
                                    'id', subfield_name)
                            cache[field_name] = dict(
                                (i, text_type(x)) for i, x in pairs)
                            cache[field_name][None] = u''
                        row.append(cache[field_name][field_id])
                    elif point_match:
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
                for col in extra_columns:
                    row.append(obj.extra_data.get(col, u''))
                rows.append(row)
                if len(rows) % batch_size == 0:  # pragma: no cover
                    write_rows()
                    count += len(rows)
                    logger.info(
                        "Exported %d %s",
                        count, objects.model._meta.verbose_name_plural)
                    rows = []

        # Write rows smaller than batch size
        write_rows()
        return out.getvalue()
