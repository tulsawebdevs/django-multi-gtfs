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

"""
Define Stop model for rows in stops.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

stops.txt is required

- stop_id (required)
The stop_id field contains an ID that uniquely identifies a stop or station.
Multiple routes may use the same stop. The stop_id is dataset unique.

- stop_code (optional)
The stop_code field contains short text or a number that uniquely identifies
the stop for passengers. Stop codes are often used in phone-based transit
information systems or printed on stop signage to make it easier for riders to
get a stop schedule or real-time arrival information for a particular stop.

The stop_code field should only be used for stop codes that are displayed to
passengers. For internal codes, use stop_id. This field should be left blank
for stops without a code.

- stop_name (required)
The stop_name field contains the name of a stop or station. Please use a name
that people will understand in the local and tourist vernacular.

- stop_desc (optional)
The stop_desc field contains a description of a stop. Please provide useful,
quality information. Do not simply duplicate the name of the stop.

- stop_lat (required)
The stop_lat field contains the latitude of a stop or station. The field value
must be a valid WGS 84 latitude.

- stop_lon (required)
The stop_lon field contains the longitude of a stop or station. The field value
must be a valid WGS 84 longitude value from -180 to 180.

- zone_id (optional)
The zone_id field defines the fare zone for a stop ID. Zone IDs are required if
you want to provide fare information using fare_rules.txt. If this stop ID
represents a station, the zone ID is ignored.

- stop_url (optional)
The stop_url field contains the URL of a web page about a particular stop. This
should be different from the agency_url and the route_url fields.

The value must be a fully qualified URL that includes http:// or https://, and
any special characters in the URL must be correctly escaped. See
  http://www.w3.org/Addressing/URL/4_URI_Recommentations.html
for a description of how to create fully qualified URL values.

- location_type (optional)
The location_type field identifies whether this stop ID represents a stop or
station. If no location type is specified, or the location_type is blank, stop
IDs are treated as stops. Stations may have different properties from stops
when they are represented on a map or used in trip planning.

The location type field can have the following values:

    * 0 or blank - Stop. A location where passengers board or disembark from a
        transit vehicle.
    * 1 - Station. A physical structure or area that contains one or more stop.

- parent_station (optional)
For stops that are physically located inside stations, the parent_station field
identifies the station associated with the stop. To use this field, stops.txt
must also contain a row where this stop ID is assigned location type=1.

If this stop ID represents a stop located inside a station, this entry's
location type should be 0 or blank, and the entry's parent_station field
contains the stop ID of the station where this stop is located. The stop
referenced by parent_station must have location_type=1.

If this stop ID represents a stop located outside a station, this entry's
location type should be 0 or blank, and the entry's parent_station field
contains a blank value. The parent_station field doesn't apply to this stop.

If this stop ID represents a station, this entry's location type should be 1,
and the entry's parent_station field should be a blank value. Stations can't
contain other stations.

- stop_timezone (optional)
The stop_timezone field contains the timezone in which this stop or station is
located. Please refer to Wikipedia List of Timezones for a list of valid
values:
  http://en.wikipedia.org/wiki/List_of_tz_zones

If omitted, the stop should be assumed to be located in the timezone specified
by agency_timezone in agency.txt.

When a stop has a parent station, the stop is considered to be in the timezone
specified by the parent station's stop_timezone value. If the parent has no
stop_timezone value, the stops that belong to that station are assumed to be in
the timezone specified by agency_timezone, even if the stops have their own
stop_timezone values. In other words, if a given stop has a parent_station
value, any stop_timezone value specified for that stop must be ignored.

Even if stop_timezone values are provided in stops.txt, the times in
stop_times.txt should continue to be specified as time since midnight in the
timezone specified by agency_timezone in agency.txt. This ensures that the time
values in a trip always increase over the course of a trip, regardless of which
timezones the trip crosses.

- wheelchair_boarding (optional)
The wheelchair_boarding field identifies whether wheelchair boardings are
possible from the specified stop or station. The field can have the following
values:

    * 0 (or empty) - indicates that there is no accessibility information for
        the stop
    * 1 - indicates that at least some vehicles at this stop can be boarded
        by a rider in a wheelchair
    * 2 - wheelchair boarding is not possible at this stop

When a stop is part of a larger station complex, as indicated by a stop with a
parent_station value, the stop's wheelchair_boarding field has the following
additional semantics:

    * 0 (or empty) - the stop will inherit its wheelchair_boarding value from
        the parent station, if specified in the parent
    * 1 - there exists some accessible path from outside the station to the
        specific stop / platform
    * 2 - there exists no accessible path from outside the station to the
        specific stop / platform
"""
from __future__ import unicode_literals
from csv import DictReader, DictWriter
from logging import getLogger
import warnings

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import StringIO

from multigtfs.models.base import models, Base


logger = getLogger(__name__)


@python_2_unicode_compatible
class Stop(Base):
    """A stop or station"""
    feed = models.ForeignKey('Feed')
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
        max_length=255, blank=True,
        help_text='Description of a stop.')
    point = models.PointField(
        help_text='WGS 84 latitude/longitude of stop or station')
    zone = models.ForeignKey(
        'Zone', null=True, blank=True,
        help_text="Fare zone for a stop ID.")
    url = models.URLField(
        blank=True, help_text="URL for the stop")
    location_type = models.CharField(
        max_length=1, blank=True, choices=(('0', 'Stop'), ('1', 'Station')),
        help_text="Is this a stop or station?")
    parent_station = models.ForeignKey(
        'Stop', null=True, blank=True,
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
        def writeheader(writer):
            '''
            Write the header row for a DictWriter CSV file

            This is a member function of DictWriter in Python 2.7
            '''
            writer.writerow(dict((fn, fn) for fn in writer.fieldnames))

        txt = txt_file.read()
        reader = DictReader(StringIO(txt))

        # Find extra fieldnames
        fieldnames = [c for c, _ in cls._column_map]
        for fieldname in reader.fieldnames:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)

        # Setup filtered CSVs
        has_stations = False
        stations_csv = StringIO()
        stations = DictWriter(stations_csv, fieldnames)
        has_stops = False
        stops_csv = StringIO()
        stops = DictWriter(stops_csv, fieldnames)

        # Filter rows into stations and stops
        for row in reader:
            if row.get('location_type') == '1':
                if not has_stations:
                    writeheader(stations)
                    has_stations = True
                stations.writerow(row)
            else:
                if not has_stops:
                    writeheader(stops)
                    has_stops = True
                stops.writerow(row)

        # Read ordered CSVs with standard importer
        total = 0
        if has_stations:
            logger.info("Importing station stops")
            total += super(Stop, cls).import_txt(
                StringIO(stations_csv.getvalue()), feed)
        if has_stops:
            logger.info("Importing non-station stops")
            total += super(Stop, cls).import_txt(
                StringIO(stops_csv.getvalue()), feed)
        return total


@receiver(post_save, sender=Stop, dispatch_uid="post_save_stop")
def post_save_stop(sender, instance, **kwargs):
    '''Update related objects when the Stop is updated'''
    from multigtfs.models.trip import Trip
    trip_ids = instance.stoptime_set.filter(
        trip__shape=None).values_list('trip_id', flat=True).distinct()
    for trip in Trip.objects.filter(id__in=trip_ids):
        trip.update_geometry()
