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
The monday field contains a binary value that indicates whether the service is valid for all Mondays.

    * A value of 1 indicates that service is available for all Mondays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Mondays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- tuesday (required)
The tuesday field contains a binary value that indicates whether the service is valid for all Tuesdays.

    * A value of 1 indicates that service is available for all Tuesdays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Tuesdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- wednesday (required)
The wednesday field contains a binary value that indicates whether the service is valid for all Wednesdays.

    * A value of 1 indicates that service is available for all Wednesdays in
      the date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Wednesdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- thursday (required)
The thursday field contains a binary value that indicates whether the service is valid for all Thursdays.

    * A value of 1 indicates that service is available for all Thursdays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Thursdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- friday (required)
The friday field contains a binary value that indicates whether the service is valid for all Fridays.

    * A value of 1 indicates that service is available for all Fridays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Fridays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- saturday (required)
The saturday field contains a binary value that indicates whether the service is valid for all Saturdays.

    * A value of 1 indicates that service is available for all Saturdays in the
      date range. (The date range is specified using the start_date and
      end_date fields.)
    * A value of 0 indicates that service is not available on Saturdays in the
      date range.

Note: You may list exceptions for particular dates, such as holidays, in the
calendar_dates.txt file.

- sunday (required)
The sunday field contains a binary value that indicates whether the service is valid for all Sundays.

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
The end_date field contains the end date for the service. This date is included in the service interval.

The end_date field's value should be in YYYYMMDD format.
"""

from django.db import models


class Service(models.Model):
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

    def __unicode__(self):
        return u"%d-%s" % (self.feed.id, self.service_id)

    class Meta:
        db_table = 'service'
        app_label = 'multigtfs'
