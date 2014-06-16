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
Define FareRule model for rows in fare_rules.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

fare_rules.txt is optional

The fare_rules table allows you to specify how fares in fare_attributes.txt
apply to an itinerary. Most fare structures use some combination of the
following rules:

 * Fare depends on origin or destination stations.
 * Fare depends on which zones the itinerary passes through.
 * Fare depends on which route the itinerary uses.

For examples that demonstrate how to specify a fare structure with
fare_rules.txt and fare_attributes.txt, see FareExamples in the
GoogleTransitDataFeed open source project wiki.

- fare_id (required)
The fare_id field contains an ID that uniquely identifies a fare class. This
value is referenced from the fare_attributes.txt file.

- route_id (optional)
The route_id field associates the fare ID with a route. Route IDs are
referenced from the routes.txt file. If you have several routes with the same
fare attributes, create a row in fare_rules.txt for each route.

For example, if fare class "b" is valid on route "TSW" and "TSE", the
fare_rules.txt file would contain these rows for the fare class:

    b,TSW
    b,TSE

- origin_id (optional)
The origin_id field associates the fare ID with an origin zone ID. Zone IDs are
referenced from the stops.txt file. If you have several origin IDs with the
same fare attributes, create a row in fare_rules.txt for each origin ID.

For example, if fare class "b" is valid for all travel originating from either
zone "2" or zone "8", the fare_rules.txt file would contain these rows for the
fare class:

    b, , 2
    b, , 8

- destination_id (optional)
The destination_id field associates the fare ID with a destination zone ID.
Zone IDs are referenced from the stops.txt file. If you have several
destination IDs with the same fare attributes, create a row in fare_rules.txt
for each destination ID.

For example, you could use the origin_ID and destination_ID fields together to
specify that fare class "b" is valid for travel between zones 3 and 4, and for
travel between zones 3 and 5, the fare_rules.txt file would contain these rows
for the fare class:

    b, , 3,4
    b, , 3,5

- contains_id (optional)
The contains_id field associates the fare ID with a zone ID, referenced from
the stops.txt file. The fare ID is then associated with itineraries that pass
through every contains_id zone.

For example, if fare class "c" is associated with all travel on the GRT route
that passes through zones 5, 6, and 7 the fare_rules.txt would contain these
rows:

    c,GRT,,,5
    c,GRT,,,6
    c,GRT,,,7

Because all contains_id zones must be matched for the fare to apply, an
itinerary that passes through zones 5 and 6 but not zone 7 would not have fare
class "c". For more detail, see FareExamples in the GoogleTransitDataFeed
project wiki:
  http://code.google.com/p/googletransitdatafeed/wiki/FareExamples
"""

from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class FareRule(Base):
    """Associate a Fare with a Route and/or Zones"""
    fare = models.ForeignKey('Fare')
    route = models.ForeignKey(
        'Route', null=True, blank=True,
        help_text="Fare class is valid for this route.")
    origin = models.ForeignKey(
        'Zone', null=True, blank=True,
        related_name='fare_origins',
        help_text="Fare class is valid for travel originating in this zone.")
    destination = models.ForeignKey(
        'Zone', null=True, blank=True,
        related_name='fare_destinations',
        help_text="Fare class is valid for travel ending in this zone.")
    contains = models.ForeignKey(
        'Zone', null=True, blank=True,
        related_name='fare_contains',
        help_text="Fare class is valid for travel withing this zone.")

    def __str__(self):
        u = "%d-%s" % (self.fare.feed.id, self.fare.fare_id)
        if self.route:
            u += '-%s' % self.route.route_id
        return u

    class Meta:
        db_table = 'fare_rules'
        app_label = 'multigtfs'

    # For Base import/export
    _column_map = (
        ('fare_id', 'fare__fare_id'),
        ('route_id', 'route__route_id'),
        ('origin_id', 'origin__zone_id'),
        ('destination_id', 'destination__zone_id'),
        ('contains_id', 'contains__zone_id')
    )
    _filename = 'fare_rules.txt'
    _rel_to_feed = 'fare__feed'
    _sort_order = ('route__route_id', 'fare__fare_id')
    _unique_fields = (
        'fare_id', 'route_id', 'origin_id', 'destination_id', 'contains_id')
