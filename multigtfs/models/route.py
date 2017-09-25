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

from django.contrib.gis.geos import MultiLineString
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Route(Base):
    """A transit route

    Maps to route.txt in the GTFS feed.
    """

    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    route_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for route.")
    agency = models.ForeignKey(
        'Agency', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Agency for this route.")
    short_name = models.CharField(
        max_length=63,
        help_text="Short name of the route")
    long_name = models.CharField(
        max_length=255,
        help_text="Long name of the route")
    desc = models.TextField(
        "description",
        blank=True,
        help_text="Long description of a route")
    rtype = models.IntegerField(
        "route type",
        choices=((0, 'Tram, Streetcar, or Light rail'),
                 (1, 'Subway or Metro'),
                 (2, 'Rail'),
                 (3, 'Bus'),
                 (4, 'Ferry'),
                 (5, 'Cable car'),
                 (6, 'Gondola or Suspended cable car'),
                 (7, 'Funicular')),
        help_text='Type of transportation used on route')
    url = models.URLField(
        blank=True, help_text="Web page about for the route")
    color = models.CharField(
        max_length=6, blank=True,
        help_text="Color of route in hex")
    text_color = models.CharField(
        max_length=6, blank=True,
        help_text="Color of route text in hex")
    geometry = models.MultiLineStringField(
        null=True, blank=True,
        help_text='Geometry cache of Trips')
    extra_data = JSONField(default={}, blank=True, null=True)

    def update_geometry(self):
        """Update the geometry from the Trips"""
        original = self.geometry
        trips = self.trip_set.exclude(geometry__isnull=True)
        unique_coords = set()
        unique_geom = list()
        for t in trips:
            coords = t.geometry.coords
            if coords not in unique_coords:
                unique_coords.add(coords)
                unique_geom.append(t.geometry)
        self.geometry = MultiLineString(unique_geom)
        if self.geometry != original:
            self.save()

    def __str__(self):
        return "%d-%s" % (self.feed.id, self.route_id)

    class Meta:
        db_table = 'route'
        app_label = 'multigtfs'

    _column_map = (
        ('route_id', 'route_id'),
        ('agency_id', 'agency__agency_id'),
        ('route_short_name', 'short_name'),
        ('route_long_name', 'long_name'),
        ('route_desc', 'desc'),
        ('route_type', 'rtype'),
        ('route_url', 'url'),
        ('route_color', 'color'),
        ('route_text_color', 'text_color')
    )
    _filename = 'routes.txt'
    _sort_order = ('route_id', 'short_name')
    _unique_fields = ('route_id',)
