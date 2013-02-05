#
# Copyright 2012 John Whitlock
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

from datetime import time
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Route, Stop, StopTime, Trip


class StopTimeTest(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create()
        self.route = Route.objects.create(
            feed=self.feed, route_id='R1', rtype=3)
        self.trip = Trip.objects.create(route=self.route, trip_id='STBA')
        self.stop = Stop.objects.create(
            feed=self.feed, stop_id='STAGECOACH', lat="36.425288",
            lon="-117.133162")

    def test_string(self):
        stoptime = StopTime.objects.create(
            trip=self.trip, stop=self.stop, arrival_time=time(6),
            departure_time=time(6), stop_sequence=1)
        self.assertEqual(str(stoptime), '1-R1-STBA-STAGECOACH-1')

    def test_import_stop_times_txt_minimal(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
STBA,6:00:00,6:00:00,STAGECOACH,1
""")
        StopTime.import_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(str(stoptime.arrival_time), '06:00:00')
        self.assertEqual(str(stoptime.departure_time), '06:00:00')
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, '')
        self.assertEqual(stoptime.pickup_type, '')
        self.assertEqual(stoptime.drop_off_type, '')
        self.assertEqual(stoptime.shape_dist_traveled, None)

    def test_import_stop_times_txt_bad_column_empty_OK(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,drop_off_time
STBA,6:00:00,6:00:00,STAGECOACH,1,
""")
        StopTime.import_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(str(stoptime.arrival_time), '06:00:00')
        self.assertEqual(str(stoptime.departure_time), '06:00:00')
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.drop_off_type, '')

    def test_import_stop_times_txt_bad_column_populated_raises(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,drop_off_time
STBA,6:00:00,6:00:00,STAGECOACH,1,1
""")
        self.assertRaises(
            ValueError, StopTime.import_txt, stop_times_txt, self.feed)

    def test_import_stop_times_txt_maximal(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,\
pickup_type,drop_off_type,shape_dist_traveled
STBA,6:00:00,6:00:00,STAGECOACH,1,"SC",2,1,5.25
""")
        StopTime.import_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(str(stoptime.arrival_time), '06:00:00')
        self.assertEqual(str(stoptime.departure_time), '06:00:00')
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, 'SC')
        self.assertEqual(stoptime.pickup_type, '2')
        self.assertEqual(stoptime.drop_off_type, '1')
        self.assertEqual(stoptime.shape_dist_traveled, 5.25)

    def test_import_stop_times_txt_empty_optional(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,\
pickup_type,drop_off_type,shape_dist_traveled
STBA,6:00:00,6:00:00,STAGECOACH,1,,,,
""")
        StopTime.import_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(str(stoptime.arrival_time), '06:00:00')
        self.assertEqual(str(stoptime.departure_time), '06:00:00')
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, '')
        self.assertEqual(stoptime.pickup_type, '')
        self.assertEqual(stoptime.drop_off_type, '')
        self.assertEqual(stoptime.shape_dist_traveled, None)

    def test_import_stop_times_txt_middle_times_optional(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
STBA,6:00:00,6:00:00,STAGECOACH,1
STBA,,,STAGECOACH2,2
STBA,12:00:00,12:00:00,STAGECOACH3,3
""")
        stop2 = Stop.objects.create(
            feed=self.feed, stop_id='STAGECOACH2', lat="36.425288",
            lon="-117.133162")
        stop3 = Stop.objects.create(
            feed=self.feed, stop_id='STAGECOACH3', lat="36.425288",
            lon="-117.133162")
        StopTime.import_txt(stop_times_txt, self.feed)
        stoptime1 = StopTime.objects.get(stop=self.stop)
        self.assertEqual(str(stoptime1.arrival_time), '06:00:00')
        self.assertEqual(str(stoptime1.departure_time), '06:00:00')
        stoptime2 = StopTime.objects.get(stop=stop2)
        self.assertEqual(stoptime2.arrival_time, None)
        self.assertEqual(stoptime2.departure_time, None)
        stoptime3 = StopTime.objects.get(stop=stop3)
        self.assertEqual(str(stoptime3.arrival_time), '12:00:00')
        self.assertEqual(str(stoptime3.departure_time), '12:00:00')

    def test_import_stop_times_txt_tomorrow(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
STBA,23:59:00,24:01:00,STAGECOACH,1
""")
        StopTime.import_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(str(stoptime.arrival_time), '23:59:00')
        self.assertEqual(str(stoptime.departure_time), '24:01:00')
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, '')
        self.assertEqual(stoptime.pickup_type, '')
        self.assertEqual(stoptime.drop_off_type, '')
        self.assertEqual(stoptime.shape_dist_traveled, None)

    def test_export_stop_times_none(self):
        stop_times_txt = StopTime.objects.in_feed(self.feed).export_txt()
        self.assertFalse(stop_times_txt)

    def test_export_stop_times_minimal(self):
        StopTime.objects.create(
            trip=self.trip, arrival_time='6:00:00', departure_time='6:00:00',
            stop=self.stop, stop_sequence=1)
        stop_times_txt = StopTime.objects.in_feed(self.feed).export_txt()
        self.assertEqual(stop_times_txt, """\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
STBA,06:00:00,06:00:00,STAGECOACH,1
""")

    def test_export_stop_times_maximal(self):
        StopTime.objects.create(
            trip=self.trip, arrival_time='6:00:00', departure_time='6:00:00',
            stop=self.stop, stop_sequence=1, stop_headsign='SC',
            pickup_type=2, drop_off_type=1, shape_dist_traveled=5.25)
        stop_times_txt = StopTime.objects.in_feed(self.feed).export_txt()
        self.assertEqual(stop_times_txt, """\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,\
pickup_type,drop_off_type,shape_dist_traveled
STBA,06:00:00,06:00:00,STAGECOACH,1,SC,2,1,5.25
""")

    def test_export_natural_sort(self):
        StopTime.objects.create(
            trip=self.trip, arrival_time='6:00:00', departure_time='6:00:00',
            stop=self.stop, stop_sequence=1, stop_headsign='SC',
            pickup_type=2, drop_off_type=1, shape_dist_traveled=5.25)
        stop2 = Stop.objects.create(
            feed=self.feed, stop_id='SALOON', lat="36.5", lon="-117.1")
        StopTime.objects.create(trip=self.trip, stop=stop2, stop_sequence=2)
        stop3 = Stop.objects.create(
            feed=self.feed, stop_id='GENERAL_STORE', lat="36.5", lon="-117.2")
        StopTime.objects.create(trip=self.trip, stop=stop3, stop_sequence=3)
        stop4 = Stop.objects.create(
            feed=self.feed, stop_id='MORGUE', lat="36.6", lon="-117.2")
        StopTime.objects.create(
            trip=self.trip, arrival_time='7:00:00', departure_time='7:00:00',
            stop=stop4, stop_sequence=4, stop_headsign='MORT')
        stop_times_txt = StopTime.objects.in_feed(self.feed).export_txt()
        self.assertEqual(stop_times_txt, """\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,\
pickup_type,drop_off_type,shape_dist_traveled
STBA,06:00:00,06:00:00,STAGECOACH,1,SC,2,1,5.25
STBA,,,SALOON,2,,,,
STBA,,,GENERAL_STORE,3,,,,
STBA,07:00:00,07:00:00,MORGUE,4,MORT,,,
""")
