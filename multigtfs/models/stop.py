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
from logging import getLogger
import warnings

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import StringIO
from jsonfield import JSONField

from multigtfs.models.base import models, Base


logger = getLogger(__name__)


@python_2_unicode_compatible
class Stop(Base):
    """A stop or station

    Maps to stops.txt in the GTFS feed.
    """
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    stop_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for a stop or station.")
    code = models.CharField(
        max_length=255, blank=True,
        help_text="Uniquer identifier (short text or number) for passengers.")
    name = models.CharField(
        max_length=255,
        help_text="Name of stop in local vernacular.")
    desc = models.CharField(
        "description",
        max_length=255, blank=True,
        help_text='Description of a stop.')
    point = models.PointField(
        help_text='WGS 84 latitude/longitude of stop or station')
    zone = models.ForeignKey(
        'Zone', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Fare zone for a stop ID.")
    url = models.URLField(
        blank=True, help_text="URL for the stop")
    location_type = models.CharField(
        max_length=1, blank=True, choices=(('0', 'Stop'), ('1', 'Station')),
        help_text="Is this a stop or station?")
    parent_station = models.ForeignKey(
        'Stop', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="The station associated with the stop")
    timezone = models.CharField(
        max_length=255, blank=True,
        help_text="Timezone of the stop")
    wheelchair_boarding = models.CharField(
        max_length=1, blank=True,
        choices=(
            ('0', 'No information'),
            ('1', 'Some wheelchair boarding'),
            ('2', 'No wheelchair boarding')),
        help_text='Is wheelchair boarding possible?')
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "%d-%s" % (self.feed_id, self.stop_id)

    def getlon(self):
        return self.point[0] if self.point else 0.0

    def setlon(self, value):
        if self.point:
            self.point[0] = value
        else:
            self.point = "POINT(%s 0)" % value

    lon = property(getlon, setlon, doc="WGS 84 longitude of stop or station")

    def getlat(self):
        return self.point[1] if self.point else 0.0

    def setlat(self, value):
        if self.point:
            self.point[1] = value
        else:
            self.point = "POINT(0 %s)" % value

    lat = property(getlat, setlat, doc="WGS 84 latitude of stop or station")

    def __init__(self, *args, **kwargs):
        lat = kwargs.pop('lat', None)
        lon = kwargs.pop('lon', None)
        if lat is not None or lon is not None:
            assert kwargs.get('point') is None
            msg = "Setting Stop location with lat and lon is deprecated"
            warnings.warn(msg, DeprecationWarning)
            kwargs['point'] = "POINT(%s %s)" % (lon or 0.0, lat or 0.0)
        super(Stop, self).__init__(*args, **kwargs)

    class Meta:
        db_table = 'stop'
        app_label = 'multigtfs'

    _column_map = (
        ('stop_id', 'stop_id'),
        ('stop_code', 'code'),
        ('stop_name', 'name'),
        ('stop_desc', 'desc'),
        ('stop_lat', 'point[1]'),
        ('stop_lon', 'point[0]'),
        ('zone_id', 'zone__zone_id'),
        ('stop_url', 'url'),
        ('location_type', 'location_type'),
        ('parent_station', 'parent_station__stop_id'),
        ('stop_timezone', 'timezone'),
        ('wheelchair_boarding', 'wheelchair_boarding'),
    )
    _filename = 'stops.txt'
    _unique_fields = ('stop_id',)

    @classmethod
    def import_txt(cls, txt_file, feed):
        '''Import from a stops.txt file

        Stations need to be imported before stops
        '''

        txt = txt_file.read()

        def is_station(pairs):
            '''Does the row represent a station?'''
            for name, val in pairs:
                if name == 'location_type':
                    return val == '1'
            return False

        logger.info("Importing station stops")
        stations = super(Stop, cls).import_txt(StringIO(txt), feed, is_station)
        logger.info("Imported %d station stops", stations)

        def is_stop(pairs):
            '''Does the row represent a stop?'''
            for name, val in pairs:
                if name == 'location_type':
                    return val != '1'
            return True

        logger.info("Importing non-station stops")
        stops = super(Stop, cls).import_txt(StringIO(txt), feed, is_stop)
        logger.info("Imported %d non-station stops", stops)
        return stations + stops


@receiver(post_save, sender=Stop, dispatch_uid="post_save_stop")
def post_save_stop(sender, instance, **kwargs):
    '''Update related objects when the Stop is updated'''
    from multigtfs.models.trip import Trip
    trip_ids = instance.stoptime_set.filter(
        trip__shape=None).values_list('trip_id', flat=True).distinct()
    for trip in Trip.objects.filter(id__in=trip_ids):
        trip.update_geometry()
