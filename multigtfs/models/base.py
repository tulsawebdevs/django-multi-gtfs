from csv import DictReader
from datetime import datetime

from django.db import models
from django.db.models.query import QuerySet

from multigtfs.utils import create_csv


class GTFSBaseQuerySet(QuerySet):
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
        return create_csv(self, csv_names)


class GTFSBaseManager(models.Manager):

    def get_query_set(self):
        return GTFSBaseQuerySet(self.model)

    def in_feed(self, feed):
        '''Return the objects in the target feed'''
        kwargs = {self.model._rel_to_feed: feed}
        return self.filter(**kwargs)


class GTFSBase(models.Model):
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

    objects = GTFSBaseManager()

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
            if isinstance(field, models.DateField):
                converter = date_convert
            elif isinstance(field, models.BooleanField):
                converter = bool_convert
            elif isinstance(field, models.CharField):
                converter = char_convert
            elif field.rel:
                converter = instance_convert(field, feed, rel_name)
            elif field.null:
                converter = null_convert
            else:
                converter = no_convert
            val_map[csv_name] = converter

        # Read and convert the source txt
        reader = DictReader(txt_file)
        for row in reader:
            fields = dict()
            if cls._rel_to_feed == 'feed':
                fields['feed'] = feed
            for column_name, value in row.items():
                if not column_name in name_map:
                    if value:
                        raise ValueError(
                            'Unexpected column name %s in row %s, expecting'
                            ' %s' % (column_name, row, name_map.keys()))
                else:
                    fields[name_map[column_name]] = val_map[column_name](value)
            cls.objects.create(**fields)
