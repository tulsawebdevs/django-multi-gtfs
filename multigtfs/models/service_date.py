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
class ServiceDate(Base):
    """Dates that a route is active.

    Implements calendar_dates.txt
    """
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    date = models.DateField(
        help_text="Date that the service differs from the norm.")
    exception_type = models.IntegerField(
        default=1, choices=((1, 'Added'), (2, 'Removed')),
        help_text="Is service added or removed on this date?")
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return (
            "%d-%s %s %s" % (
                self.service.feed.id, self.service.service_id, self.date,
                'Added' if self.exception_type == 1 else 'Removed'))

    class Meta:
        db_table = 'service_date'
        app_label = 'multigtfs'

    # For Base import/export
    _column_map = (
        ('service_id', 'service__service_id'),
        ('date', 'date'),
        ('exception_type', 'exception_type'))
    _filename = 'calendar_dates.txt'
    _rel_to_feed = 'service__feed'
    _sort_order = ('date', 'exception_type')
    _unique_fields = ('service_id', 'date')
