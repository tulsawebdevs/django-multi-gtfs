"""
Define Frequency model for rows in frequencies.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

frequencies.txt is optional.

This table is intended to represent schedules that don't have a fixed list of
stop times. When trips are defined in frequencies.txt, the trip planner ignores
the absolute values of the arrival_time and departure_time fields for those
trips in stop_times.txt. Instead, the stop_times table defines the sequence of
stops and the time difference between each stop.

- trip_id (required)
The trip_id contains an ID that identifies a trip on which the specified
frequency of service applies. Trip IDs are referenced from the trips.txt file.

- start_time (required)
The start_time field specifies the time at which service begins with the
specified frequency. The time is measured from "noon minus 12h" (effectively
midnight, except for days on which daylight savings time changes occur) at the
beginning of the service date. For times occurring after midnight, enter the
time as a value greater than 24:00:00 in HH:MM:SS local time for the day on
which the trip schedule begins. E.g. 25:35:00.

- end_time (required)
The end_time field indicates the time at which service changes to a different
frequency (or ceases) at the first stop in the trip. The time is measured from
"noon minus 12h" (effectively midnight, except for days on which daylight
savings time changes occur) at the beginning of the service date. For times
occurring after midnight, enter the time as a value greater than 24:00:00 in
HH:MM:SS local time for the day on which the trip schedule begins. E.g.
25:35:00.

- headway_secs (required)
The headway_secs field indicates the time between departures from the same stop
(headway) for this trip type, during the time interval specified by start_time
and end_time. The headway value must be entered in seconds.

Periods in which headways are defined (the rows in frequencies.txt) shouldn't
overlap for the same trip, since it's hard to determine what should be inferred
from two overlapping headways. However, a headway period may begin at the exact
same time that another one ends, for instance:

    A, 05:00:00, 07:00:00, 600
    B, 07:00:00, 12:00:00, 1200

- exact_times (optional)
The exact_times field determines if frequency-based trips should be exactly
scheduled based on the specified headway information. Valid values for this
field are:

  * 0 or (empty) - Frequency-based trips are not exactly scheduled. This is the
    default behavior.
  * 1 - Frequency-based trips are exactly scheduled. For a frequencies.txt row,
    trips are scheduled starting with
    trip_start_time = start_time + x * headway_secs for all x in (0, 1, 2, ...)
    where trip_start_time < end_time.

The value of exact_times must be the same for all frequencies.txt rows with the
same trip_id. If exact_times is 1 and a frequencies.txt row has a start_time
equal to end_time, no trip must be scheduled. When exact_times is 1, care must
be taken to choose an end_time value that is greater than the last desired trip
start time but less than the last desired trip start time + headway_secs.
"""

from django.db import models

from multigtfs.models.base import GTFSBase
from multigtfs.models.fields import GTFSSecondsField


class Frequency(GTFSBase):
    """Description of a trip that repeats without fixed stop times"""
    trip = models.ForeignKey('Trip')
    start_time = GTFSSecondsField(
        help_text="Time that the service begins at the specified frequency")
    end_time = GTFSSecondsField(
        help_text="Time that the service ends at the specified frequency")
    headway_secs = models.IntegerField(
        help_text="Time in seconds before returning to same stop")
    exact_times = models.CharField(
        max_length=1, blank=True,
        choices=((0, 'Trips are not exactly scheduled'),
                 (1, 'Trips are exactly scheduled from start time')),
        help_text="Should frequency-based trips be exactly scheduled?")

    def __unicode__(self):
        return unicode(self.trip)

    class Meta:
        db_table = 'frequency'
        app_label = 'multigtfs'
        verbose_name_plural = "frequencies"

    # For GTFSBase import/export
    _column_map = (
        ('trip_id', 'trip__trip_id'),
        ('start_time', 'start_time'),
        ('end_time', 'end_time'),
        ('headway_secs', 'headway_secs'),
        ('exact_times', 'exact_times'))
    _rel_to_feed = 'trip__route__feed'

#
# def import_frequencies_txt(frequencies_file, feed):
#     """Import frequencies.txt into Frequency records for feed
#
#     Keyword arguments:
#     frequencies_file -- A open frequencies.txt for reading
#     feed -- the Feed to associate the records with
#     """
#     reader = DictReader(frequencies_file)
#     for row in reader:
#         trip_id = row.pop('trip_id')
#         trip = Trip.objects.get(route__feed=feed, trip_id=trip_id)
#         # Convert times
#         stime, sday = parse_time(row.pop('start_time', None))
#         etime, eday = parse_time(row.pop('end_time', None))
#         Frequency.objects.create(
#             trip=trip, start_time=stime, start_day=sday, end_time=etime,
#             end_day=eday, **row)
