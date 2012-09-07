"Define model and field to represent time of day in GTFS feeds"

from django.db import models


class GTFSSeconds(object):
    '''A GTFS seconds value, formatted as HH:MM:SS in the GTFS feed'''

    def __init__(self, seconds=0):
        self.seconds = int(seconds)
        if self.seconds < 0:
            raise ValueError('seconds must be positive')

    @classmethod
    def from_hms(cls, hours=0, minutes=0, seconds=0):
        return GTFSSeconds((hours * 60 * 60) + (minutes * 60) + seconds)

    def __unicode__(self):
        minutes, seconds = divmod(self.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return u"%02d:%02d:%02d" % (hours, minutes, seconds)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __cmp__(self, other):
        if isinstance(other, self.__class__):
            return self.seconds.__cmp__(other.seconds)
        else:
            return -1

    def __ne__(self, other):
        return not (self == other)


class GTFSSecondsField(models.Field):
    '''A Model Field for storing GTFSSeconds'''

    description = 'Seconds since start of the day'

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, GTFSSeconds):
            return value
        if value is None:
            return None
        if isinstance(value, (int, long)):
            return GTFSSeconds(value)
        svalue = str(value)
        colons = svalue.count(':')
        if colons == 2:
            hours, minutes, seconds = [int(v) for v in svalue.split(':')]
        elif colons == 1:
            hours, minutes = [int(v) for v in svalue.split(':')]
            seconds = 0
        elif colons == 0:
            hours = 0
            minutes = 0
            seconds = int(svalue)
        else:
            raise ValueError('Must be in seconds or HH:MM:SS format')
        return GTFSSeconds.from_hms(hours, minutes, seconds)

    def get_prep_value(self, value):
        if value:
            return value.seconds
        else:
            return None

    def get_internal_type(self):
        return 'IntegerField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return str(value)
