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
Define Trip model for rows in trips.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

trips.txt is required

- route_id (required)
The route_id field contains an ID that uniquely identifies a route. This value
is referenced from the routes.txt file.

- service_id (required)
The service_id contains an ID that uniquely identifies a set of dates when
service is available for one or more routes. This value is referenced from the
calendar.txt or calendar_dates.txt file.

- trip_id (required)
The trip_id field contains an ID that identifies a trip. The trip_id is dataset
unique.

- trip_headsign (optional)
The trip_headsign field contains the text that appears on a sign that
identifies the trip's destination to passengers. Use this field to distinguish
between different patterns of service in the same route. If the headsign
changes during a trip, you can override the trip_headsign by specifying values
for the the stop_headsign field in stop_times.txt.

See a Google Maps screenshot highlighting the headsign:
  http://bit.ly/A3ot2j

- trip_short_name (optional)
The trip_short_name field contains the text that appears in schedules and sign
boards to identify the trip to passengers, for example, to identify train
numbers for commuter rail trips. If riders do not commonly rely on trip names,
please leave this field blank.

A trip_short_name value, if provided, should uniquely identify a trip within a
service day; it should not be used for destination names or limited/express
designations.

- direction_id (optional)
The direction_id field contains a binary value that indicates the direction of
travel for a trip. Use this field to distinguish between bi-directional trips
with the same route_id. This field is not used in routing; it provides a way to
separate trips by direction when publishing time tables. You can specify names
for each direction with the trip_headsign field.

    * 0 - travel in one direction (e.g. outbound travel)
    * 1 - travel in the opposite direction (e.g. inbound travel)

For example, you could use the trip_headsign and direction_id fields together
to assign a name to travel in each direction on trip "1234", the trips.txt file
would contain these rows for use in time tables:

    trip_id, ... ,trip_headsign,direction_id
    1234, ... , to Airport,0
    1505, ... , to Downtown,1

- block_id (optional)
The block_id field identifies the block to which the trip belongs. A block
consists of two or more sequential trips made using the same vehicle, where a
passenger can transfer from one trip to the next just by staying in the
vehicle. The block_id must be referenced by two or more trips in trips.txt.

- shape_id (optional)
The shape_id field contains an ID that defines a shape for the trip. This value
is referenced from the shapes.txt file. The shapes.txt file allows you to
define how a line should be drawn on the map to represent a trip.

- wheelchair_accessible (optional)
    * 0 (or empty) - indicates that there is no accessibility information for
        the trip
    * 1 - indicates that the vehicle being used on this particular trip can
        accommodate at least one rider in a wheelchair
    * 2 - indicates that no riders in wheelchairs can be accommodated on this
        trip

- bikes_allowed (optional)
    * 0 (or empty) - indicates that there is no bike information for the trip
    * 1 - indicates that the vehicle being used on this particular trip can
        accommodate at least one bicycle
    * 2 - indicates that no bicycles are allowed on this trip
"""
from __future__ import unicode_literals

from django.contrib.gis.geos import LineString
from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Trip(Base):
    """A trip along a route"""

    route = models.ForeignKey('Route')
    service = models.ForeignKey('Service', null=True, blank=True)
    trip_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for a trip.")
    headsign = models.CharField(
        max_length=255, blank=True,
        help_text="Destination identification for passengers.")
    short_name = models.CharField(
        max_length=63, blank=True,
        help_text="Short name used in schedules and signboards.")
    direction = models.CharField(
        max_length=1, blank=True,
        choices=(('0', 'Outbound'), ('1', 'Inbound')),
        help_text="Direction for bi-directional routes.")
    block = models.ForeignKey(
        'Block', null=True, blank=True,
        help_text="Block of sequential trips that this trip belongs to.")
    shape = models.ForeignKey(
        'Shape', null=True, blank=True,
        help_text="Shape used for this trip")
    geometry = models.LineStringField(
        null=True, blank=True,
        help_text='Geometry cache of Shape or Stops')
    wheelchair_accessible = models.CharField(
        max_length=1, blank=True,
        choices=(
            ('0', 'No information'),
            ('1', 'Some wheelchair accommodation'),
            ('2', 'No wheelchair accommodation')),
        help_text='Are there accommodations for riders with wheelchair?')
    bikes_allowed = models.CharField(
        max_length=1, blank=True,
        choices=(
            ('0', 'No information'),
            ('1', 'Some bicycle accommodation'),
            ('2', 'No bicycles allowed')),
        help_text='Are bicycles allowed?')

    def update_geometry(self, update_parent=True):
        """Update the geometry from the Shape or Stops"""
        original = self.geometry
        if self.shape:
            self.geometry = self.shape.geometry
        else:
            stoptimes = self.stoptime_set.order_by('stop_sequence')
            if stoptimes.count() > 1:
                self.geometry = LineString(
                    [st.stop.point.coords for st in stoptimes])
        if self.geometry != original:
            self.save()
            if update_parent:
                self.route.update_geometry()

    def __str__(self):
        return "%s-%s" % (self.route, self.trip_id)

    class Meta:
        db_table = 'trip'
        app_label = 'multigtfs'

    _column_map = (
        ('route_id', 'route__route_id'),
        ('service_id', 'service__service_id'),
        ('trip_id', 'trip_id'),
        ('trip_headsign', 'headsign'),
        ('trip_short_name', 'short_name'),
        ('direction_id', 'direction'),
        ('block_id', 'block__block_id'),
        ('shape_id', 'shape__shape_id'),
        ('wheelchair_accessible', 'wheelchair_accessible'),
        ('bikes_allowed', 'bikes_allowed'),
    )
    _filename = 'trips.txt'
    _rel_to_feed = 'route__feed'
    _unique_fields = ('trip_id',)
