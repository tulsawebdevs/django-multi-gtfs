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

from django.contrib.gis.geos import LineString
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Trip(Base):
    """A trip along a route

    This implements trips.txt in the GTFS feed
    """

    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    service = models.ForeignKey(
        'Service', null=True, blank=True, on_delete=models.SET_NULL)
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
        choices=(('0', '0'), ('1', '1')),
        help_text="Direction for bi-directional routes.")
    block = models.ForeignKey(
        'Block', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Block of sequential trips that this trip belongs to.")
    shape = models.ForeignKey(
        'Shape', null=True, blank=True, on_delete=models.SET_NULL,
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
    extra_data = JSONField(default={}, blank=True, null=True)

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
