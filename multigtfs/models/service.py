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
class Service(Base):
    """Dates that a route is active.

    Implements calendar.txt
    """

    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    service_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for service dates.")
    monday = models.BooleanField(
        default=True,
        help_text="Is the route active on Monday?")
    tuesday = models.BooleanField(
        default=True,
        help_text="Is the route active on Tuesday?")
    wednesday = models.BooleanField(
        default=True,
        help_text="Is the route active on Wednesday?")
    thursday = models.BooleanField(
        default=True,
        help_text="Is the route active on Thursday?")
    friday = models.BooleanField(
        default=True,
        help_text="Is the route active on Friday?")
    saturday = models.BooleanField(
        default=True,
        help_text="Is the route active on Saturday?")
    sunday = models.BooleanField(
        default=True,
        help_text="Is the route active on Sunday?")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "%d-%s" % (self.feed.id, self.service_id)

    class Meta:
        db_table = 'service'
        app_label = 'multigtfs'

    # For Base import/export
    _column_map = (
        ('service_id', 'service_id'),
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
        ('start_date', 'start_date'),
        ('end_date', 'end_date')
    )
    _filename = 'calendar.txt'
    _sort_order = ('start_date', 'end_date')
    _unique_fields = ('service_id',)

    @classmethod
    def export_txt(cls, feed):
        '''Export records as calendar.txt'''

        # If no records with start/end dates, skip calendar.txt
        objects = cls.objects.in_feed(feed)

        if not objects.exclude(
                start_date__isnull=True, end_date__isnull=True).exists():
            return None

        return super(Service, cls).export_txt(feed)
