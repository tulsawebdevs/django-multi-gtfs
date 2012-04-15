from datetime import date, time
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Route, Service, Stop, StopTime, Trip
from multigtfs.models.stop_time import import_stop_times_txt


class StopTimesTest(TestCase):

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
        import_stop_times_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(stoptime.arrival_time, time(6))
        self.assertEqual(stoptime.departure_time, time(6))
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, '')
        self.assertEqual(stoptime.pickup_type, '')
        self.assertEqual(stoptime.drop_off_type, '')
        self.assertEqual(stoptime.shape_dist_traveled, None)

    def test_import_stop_times_txt_maximal(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled
STBA,6:00:00,6:00:00,STAGECOACH,1,"SC",2,1,5.25
""")
        import_stop_times_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(stoptime.arrival_time, time(6))
        self.assertEqual(stoptime.departure_time, time(6))
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, 'SC')
        self.assertEqual(stoptime.pickup_type, '2')
        self.assertEqual(stoptime.drop_off_type, '1')
        self.assertEqual(stoptime.shape_dist_traveled, 5.25)

    def test_import_stop_times_txt_empty_optional(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled
STBA,6:00:00,6:00:00,STAGECOACH,1,,,,
""")
        import_stop_times_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(stoptime.arrival_time, time(6))
        self.assertEqual(stoptime.departure_time, time(6))
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
        import_stop_times_txt(stop_times_txt, self.feed)
        stoptime1 = StopTime.objects.get(stop=self.stop)
        self.assertEqual(stoptime1.arrival_time, time(6))
        self.assertEqual(stoptime1.departure_time, time(6))
        stoptime2 = StopTime.objects.get(stop=stop2)
        self.assertEqual(stoptime2.arrival_time, None)
        self.assertEqual(stoptime2.departure_time, None)
        stoptime3 = StopTime.objects.get(stop=stop3)
        self.assertEqual(stoptime3.arrival_time, time(12))
        self.assertEqual(stoptime3.departure_time, time(12))

    def test_import_stop_times_txt_tomorrow(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
STBA,23:59:00,24:01:00,STAGECOACH,1
""")
        import_stop_times_txt(stop_times_txt, self.feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, self.trip)
        self.assertEqual(stoptime.arrival_time, time(23,59))
        self.assertEqual(stoptime.arrival_day, 0)
        self.assertEqual(stoptime.departure_time, time(0,1))
        self.assertEqual(stoptime.departure_day, 1)
        self.assertEqual(stoptime.stop, self.stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, '')
        self.assertEqual(stoptime.pickup_type, '')
        self.assertEqual(stoptime.drop_off_type, '')
        self.assertEqual(stoptime.shape_dist_traveled, None)