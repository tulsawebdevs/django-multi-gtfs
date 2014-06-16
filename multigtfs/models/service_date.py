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
Define ServiceDate model for rows in calendar_dates.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

calendar_dates.txt is optional

The calendar_dates table allows you to explicitly activate or disable
service IDs by date. You can use it in two ways.

Recommended: Use calendar_dates.txt in conjunction with calendar.txt, where
calendar_dates.txt defines any exceptions to the default service categories
defined in the calendar.txt file. If your service is generally regular, with a
few changes on explicit dates (for example, to accomodate special event
services, or a school schedule), this is a good approach.

Alternate: Omit calendar.txt, and include ALL dates of service in
calendar_dates.txt. If your schedule varies most days of the month, or you want
to programmatically output service dates without specifying a normal weekly
schedule, this approach may be preferable.

- service_id (required)
The service_id contains an ID that uniquely identifies a set of dates when a
service exception is available for one or more routes. Each (service_id, date)
pair can only appear once in calendar_dates.txt. If the a service_id value
appears in both the calendar.txt and calendar_dates.txt files, the information
in calendar_dates.txt modifies the service information specified in
calendar.txt. This field is referenced by the trips.txt file.

- date (required)
The date field specifies a particular date when service availability is
different than the norm. You can use the exception_type field to indicate
whether service is available on the specified date.

The date field's value should be in YYYYMMDD format.

- exception_type (required)
The exception_type indicates whether service is available on the date specified
in the date field.

  * A value of 1 indicates that service has been added for the specified date.
  * A value of 2 indicates that service has been removed for the specified
    date.

For example, suppose a route has one set of trips available on holidays and
another set of trips available on all other days. You could have one service_id
that corresponds to the regular service schedule and another service_id that
corresponds to the holiday schedule. For a particular holiday, you would use
the calendar_dates.txt file to add the holiday to the holiday service_id and to
remove the holiday from the regular service_id schedule.
"""
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class ServiceDate(Base):
    """Dates that a route is active."""

    service = models.ForeignKey('Service')
    date = models.DateField(
        help_text="Date that the service differs from the norm.")
    exception_type = models.IntegerField(
        default=1, choices=((1, 'Added'), (2, 'Removed')),
        help_text="Is service added or removed on this date?")

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
