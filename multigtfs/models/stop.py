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
"""

from csv import DictReader
from collections import defaultdict

from django.db import models

from multigtfs.models.zone import Zone


class Stop(models.Model):
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
    lat = models.DecimalField(
        'Latitude', max_digits=13, decimal_places=8,
        help_text='WGS 84 latitude of stop or station')
    lon = models.DecimalField(
        'Longitude', max_digits=13, decimal_places=8,
        help_text='WGS 84 longtitude of stop or station')
    zone = models.ForeignKey(
        'Zone', null=True,
        help_text="Fare zone for a stop ID.")
    url = models.URLField(
        verify_exists=False, blank=True,
        help_text="URL for the stop")
    location_type = models.CharField(
        max_length=1, blank=True, choices=(('0', 'Stop'), ('1', 'Station')),
        help_text="Is this a stop or station?")
    parent_station = models.ForeignKey(
        'Stop', null=True, help_text="The station associated with the stop")
    timezone = models.CharField(
        max_length=255, blank=True,
        help_text="Timezone of the stop")

    def __unicode__(self):
        return u"%d-%s" % (self.feed.id, self.stop_id)

    class Meta:
        db_table = 'stop'
        app_label = 'multigtfs'


def import_stops_txt(stops_file, feed):
    """Import stops.txt into Stop records for feed

    Keyword arguments:
    stops_file -- A open stops.txt for reading
    feed -- the Feed to associate the records with

    Zone objects may also be created, if referenced in the stops
    """
    reader = DictReader(stops_file)
    parent_of = defaultdict(list)
    name_map = dict(stop_code='code', stop_name='name', stop_desc='desc',
                    stop_lat='lat', stop_lon='lon', stop_url='url',
                    stop_timezone='timezone')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k, v in row.items())
        parent_id = fields.pop('parent_station', None)
        zone_id = fields.pop('zone_id', None)
        if zone_id:
            zone, _c = Zone.objects.get_or_create(feed=feed, zone_id=zone_id)
        else:
            zone = None
        stop = Stop.objects.create(feed=feed, zone=zone, **fields)
        if parent_id:
            parent_of[parent_id].append(stop)

    for parent_id, children in parent_of.items():
        parent = Stop.objects.get(feed=feed, stop_id=parent_id)
        for child in children:
            child.parent_station = parent
            child.save()
