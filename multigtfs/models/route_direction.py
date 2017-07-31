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

from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class RouteDirection(Base):
    """Associate a name with a Route and Direction

    Maps to non-standard route_directions.txt in GTFS feed.
    """
    route = models.ForeignKey(
        'Route', null=True, blank=True,
        help_text="Route for which this direction description applies.")
    direction = models.CharField(
        max_length=1, blank=True,
        choices=(('0', '0'), ('1', '1')),
        help_text="Direction of travel for direction description.")
    direction_name = models.CharField(
        max_length=255, blank=True,
        help_text="Destination identification for passengers.")
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        u = "%d-%s-%s" % (self.fare.feed.id, self.fare.fare_id, self.route.route_id)
        return u

    class Meta:
        db_table = 'route_directions'
        app_label = 'multigtfs'

    # For Base import/export
    _column_map = (
        ('route_id', 'route__route_id'),
        ('direction', 'direction'),
        ('direction_name', 'direction_name'),
    )
    _filename = 'route_directions.txt'
    _rel_to_feed = 'route__feed'
    _sort_order = ('route__route_id', 'direction')
    _unique_fields = ()
