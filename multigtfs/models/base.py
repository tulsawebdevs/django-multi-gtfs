# -*- coding: utf-8 -*-
# Copyright 2012-2014 John Whitlock
# Copyright 2014 Juha Yrjölä
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
from codecs import BOM_UTF8
from collections import defaultdict
from csv import reader, writer
from datetime import datetime, date
from logging import getLogger
import re

from django.contrib.gis.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils.six import StringIO, text_type, PY3

from multigtfs.compat import (
    get_blank_value, write_text_rows, Manager, QuerySet)

logger = getLogger(__name__)
re_point = re.compile(r'(?P<name>point)\[(?P<index>\d)\]')
batch_size = 1000
large_queryset_size = 100000
CSV_BOM = BOM_UTF8.decode('utf-8') if PY3 else BOM_UTF8


class BaseQuerySet(QuerySet):
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
                field = cls._meta.get_field(field_name)

            # Only add optional columns if they are used in the records
            if field and field.blank and not field.has_default():
                kwargs = {field_name: get_blank_value(field)}
                if self.exclude(**kwargs).exists():
                    column_map.append((csv_name, field_pattern))
            else:
                column_map.append((csv_name, field_pattern))
        return column_map


class BaseManager(Manager):
    def get_queryset(self):
        '''Return the custom queryset.'''
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
    def import_txt(cls, txt_file, feed, filter_func=None):
        '''Import from the GTFS text file'''

        # Setup the conversion from GTFS to Django Format
        # Conversion functions
        def no_convert(value): return value

        def date_convert(value): return datetime.strptime(value, '%Y%m%d')

        def bool_convert(value): return (value == '1')

        def char_convert(value): return (value or '')

        def null_convert(value): return (value or None)

        def point_convert(value):
            """Convert latitude / longitude, strip leading +."""
            if value.startswith('+'):
                return value[1:]
            else:
                return (value or 0.0)

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
                if value.strip():
                    related = field.related_model
                    key1 = "{}:{}".format(related.__name__, rel_name)
                    key2 = text_type(value)

                    # Load existing objects
                    if key1 not in cache:
                        pairs = related.objects.filter(
                            **{related._rel_to_feed: feed}).values_list(
                            rel_name, 'id')
                        cache[key1] = dict((text_type(x), i) for x, i in pairs)

                    # Create new?
                    if key2 not in cache[key1]:
                        kwargs = {
                            related._rel_to_feed: feed,
                            rel_name: value}
                        cache[key1][key2] = related.objects.create(
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
                field = cls._meta.get_field(field_base)

            # Pick a conversion function for the field
            if point_match:
                converter = point_convert
            elif isinstance(field, models.DateField):
                converter = date_convert
            elif isinstance(field, models.BooleanField):
                converter = bool_convert
            elif isinstance(field, models.CharField):
                converter = char_convert
            elif field.is_relation:
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
        csv_reader = reader(txt_file, skipinitialspace=True)
        unique_line = dict()
        count = 0
        first = True
        extra_counts = defaultdict(int)
        new_objects = []
        for row in csv_reader:
            if first:
                # Read the columns
                columns = row
                if columns[0].startswith(CSV_BOM):
                    columns[0] = columns[0][len(CSV_BOM):]
                first = False
                continue

            if filter_func and not filter_func(zip(columns, row)):
                continue

            if not row:
                continue

            # Read a data row
            fields = dict()
            point_coords = [None, None]
            ukey_values = {}
            if cls._rel_to_feed == 'feed':
                fields['feed'] = feed
            for column_name, value in zip(columns, row):
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
                    cls._filename, csv_reader.line_num, unique_line[ukey])
                continue
            else:
                unique_line[ukey] = csv_reader.line_num

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
            for column in columns:
                if column in extra_counts and column not in extra_columns:
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

        # Get the columns used in the dataset
        column_map = objects.populated_column_map()
        columns, fields = zip(*column_map)
        extra_columns = feed.meta.get(
            'extra_columns', {}).get(cls.__name__, [])

        # Get sort order
        if hasattr(cls, '_sort_order'):
            sort_fields = cls._sort_order
        else:
            sort_fields = []
            for field in fields:
                base_field = field.split('__', 1)[0]
                point_match = re_point.match(base_field)
                if point_match:
                    continue
                field_type = cls._meta.get_field(base_field)
                assert not isinstance(field_type, ManyToManyField)
                sort_fields.append(field)

        # Create CSV writer
        out = StringIO()
        csv_writer = writer(out, lineterminator='\n')

        # Write header row
        header_row = [text_type(c) for c in columns]
        header_row.extend(extra_columns)
        write_text_rows(csv_writer, [header_row])

        # Report the work to be done
        total = objects.count()
        logger.info(
            '%d %s to export...',
            total, cls._meta.verbose_name_plural)

        # Populate related items cache
        model_to_field_name = {}
        cache = {}
        for field_name in fields:
            if '__' in field_name:
                local_field_name, subfield_name = field_name.split('__', 1)
                field = cls._meta.get_field(local_field_name)
                field_type = field.related_model
                model_name = field_type.__name__
                if model_name in model_to_field_name:
                    # Already loaded this model under a different field name
                    cache[field_name] = cache[model_to_field_name[model_name]]
                else:
                    # Load all feed data for this model
                    pairs = field_type.objects.in_feed(
                        feed).values_list('id', subfield_name)
                    cache[field_name] = dict(
                        (i, text_type(x)) for i, x in pairs)
                    cache[field_name][None] = u''
                    model_to_field_name[model_name] = field_name

        # For large querysets, break up by the first field
        if total < large_queryset_size:
            querysets = [objects.order_by(*sort_fields)]
        else:  # pragma: no cover
            field1_raw = sort_fields[0]
            assert '__' in field1_raw
            assert field1_raw in cache
            field1 = field1_raw.split('__', 1)[0]
            field1_id = field1 + '_id'

            # Sort field1 ids by field1 values
            val_to_id = dict((v, k) for k, v in cache[field1_raw].items())
            assert len(val_to_id) == len(cache[field1_raw])
            sorted_vals = sorted(val_to_id.keys())

            querysets = []
            for val in sorted_vals:
                fid = val_to_id[val]
                if fid:
                    qs = objects.filter(
                        **{field1_id: fid}).order_by(*sort_fields[1:])
                    querysets.append(qs)

        # Assemble the rows, writing when we hit batch size
        count = 0
        rows = []
        for queryset in querysets:
            for item in queryset.order_by(*sort_fields):
                row = []
                for csv_name, field_name in column_map:
                    obj = item
                    point_match = re_point.match(field_name)
                    if '__' in field_name:
                        # Return relations from cache
                        local_field_name = field_name.split('__', 1)[0]
                        field_id = getattr(obj, local_field_name + '_id')
                        row.append(cache[field_name][field_id])
                    elif point_match:
                        # Get the lat or long from the point
                        name, index = point_match.groups()
                        field = getattr(obj, name)
                        row.append(field.coords[int(index)])
                    else:
                        # Handle other field types
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
                    write_text_rows(csv_writer, rows)
                    count += len(rows)
                    logger.info(
                        "Exported %d %s",
                        count, cls._meta.verbose_name_plural)
                    rows = []

        # Write rows smaller than batch size
        write_text_rows(csv_writer, rows)
        return out.getvalue()
