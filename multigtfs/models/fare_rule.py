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
class FareRule(Base):
    """Associate a Fare with a Route and/or Zones"""
    fare = models.ForeignKey('Fare', on_delete=models.CASCADE)
    route = models.ForeignKey(
        'Route', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Fare class is valid for this route.")
    origin = models.ForeignKey(
        'Zone', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='fare_origins',
        help_text="Fare class is valid for travel originating in this zone.")
    destination = models.ForeignKey(
        'Zone', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='fare_destinations',
        help_text="Fare class is valid for travel ending in this zone.")
    contains = models.ForeignKey(
        'Zone', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='fare_contains',
        help_text="Fare class is valid for travel withing this zone.")
    extra_data = JSONField(default={}, blank=True, null=True)

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
