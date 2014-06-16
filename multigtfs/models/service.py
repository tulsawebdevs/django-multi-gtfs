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
Define Service model for rows in calendar.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

calendar.txt is required

- service_id (required)
The service_id contains an ID that uniquely identifies a set of dates when
service is available for one or more routes. Each service_id value can appear
at most once in a calendar.txt file. This value is dataset unique. It is
referenced by the trips.txt file.

- monday (required)
The monday field contains a binary value that indicates whether the service is
valid for all Mondays.

    * A value of 1 indicates that service is available for all Mondays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Mondays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- tuesday (required)
The tuesday field contains a binary value that indicates whether the service is
valid for all Tuesdays.

    * A value of 1 indicates that service is available for all Tuesdays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Tuesdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- wednesday (required)
The wednesday field contains a binary value that indicates whether the service
is valid for all Wednesdays.

    * A value of 1 indicates that service is available for all Wednesdays in
      the date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Wednesdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- thursday (required)
The thursday field contains a binary value that indicates whether the service
is valid for all Thursdays.

    * A value of 1 indicates that service is available for all Thursdays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Thursdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- friday (required)
The friday field contains a binary value that indicates whether the service is
valid for all Fridays.

    * A value of 1 indicates that service is available for all Fridays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Fridays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- saturday (required)
The saturday field contains a binary value that indicates whether the service
is valid for all Saturdays.

    * A value of 1 indicates that service is available for all Saturdays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Saturdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- sunday (required)
The sunday field contains a binary value that indicates whether the service is
valid for all Sundays.

    * A value of 1 indicates that service is available for all Sundays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Sundays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- start_date (required)
The start_date field contains the start date for the service.

The start_date field's value should be in YYYYMMDD format.

- end_date (required)
The end_date field contains the end date for the service. This date is
included in the service interval.

The end_date field's value should be in YYYYMMDD format.
"""
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Service(Base):
    """Dates that a route is active."""

    feed = models.ForeignKey('Feed')
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
    start_date = models.DateField()
    end_date = models.DateField()

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
