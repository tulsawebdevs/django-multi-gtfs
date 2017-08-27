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
from multigtfs.models.fields import SecondsField


@python_2_unicode_compatible
class Frequency(Base):
    """Description of a trip that repeats without fixed stop times"""
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    start_time = SecondsField(
        help_text="Time that the service begins at the specified frequency")
    end_time = SecondsField(
        help_text="Time that the service ends at the specified frequency")
    headway_secs = models.IntegerField(
        help_text="Time in seconds before returning to same stop")
    exact_times = models.CharField(
        max_length=1, blank=True,
        choices=((0, 'Trips are not exactly scheduled'),
                 (1, 'Trips are exactly scheduled from start time')),
        help_text="Should frequency-based trips be exactly scheduled?")
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return str(self.trip)

    class Meta:
        db_table = 'frequency'
        app_label = 'multigtfs'
        verbose_name_plural = "frequencies"

    # For Base import/export
    _column_map = (
        ('trip_id', 'trip__trip_id'),
        ('start_time', 'start_time'),
        ('end_time', 'end_time'),
        ('headway_secs', 'headway_secs'),
        ('exact_times', 'exact_times'))
    _filename = 'frequencies.txt'
    _rel_to_feed = 'trip__route__feed'
    _unique_fields = ('trip_id', 'start_time')
