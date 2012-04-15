from datetime import date, time
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Route, Service, Stop, StopTime, Trip
from multigtfs.utils import import_stop_times


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

    def test_import_stop_times_minimal(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
STBA,6:00:00,6:00:00,STAGECOACH,1
""")
        import_stop_times(stop_times_txt, self.feed)
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

    def test_import_stop_times_maximal(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled
STBA,6:00:00,6:00:00,STAGECOACH,1,"SC",2,1,5.25
""")
        import_stop_times(stop_times_txt, self.feed)
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

    def test_import_stop_times_empty_optional(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled
STBA,6:00:00,6:00:00,STAGECOACH,1,,,,
""")
        import_stop_times(stop_times_txt, self.feed)
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
