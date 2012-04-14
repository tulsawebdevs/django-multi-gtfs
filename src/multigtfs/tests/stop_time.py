from datetime import date, time
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Route, Service, Stop, StopTime, Trip
from multigtfs.utils import import_stop_times


class StopTimeModelTest(TestCase):
    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(feed.id, 1)
        route = Route.objects.create(feed=feed, route_id='R1', rtype=3)
        trip = Trip.objects.create(route=route, trip_id='STBA')
        stop = Stop.objects.create(
            feed=feed, stop_id='STAGECOACH', lat="36.425288",
            lon="-117.133162")
        stoptime = StopTime.objects.create(
            trip=trip, stop=stop, arrival_time=time(6),
            departure_time=time(6), stop_sequence=1)
        self.assertEqual(str(stoptime), '1-R1-STBA-STAGECOACH-1')


class ImportStopTimesTest(TestCase):

    def test_import_stop_times_minimal(self):
        stop_times_txt = StringIO.StringIO("""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
STBA,6:00:00,6:00:00,STAGECOACH,1
""")
        feed = Feed.objects.create()
        route = Route.objects.create(feed=feed, route_id='R1', rtype=3)
        service = Service.objects.create(
            feed=feed, service_id='S1', start_date=date(2011,4,14), 
            end_date=date(2011,12,31))
        trip = Trip.objects.create(route=route, trip_id='STBA')
        trip.services.add(service)
        stop = Stop.objects.create(
            feed=feed, stop_id='STAGECOACH', lat="36.425288",
            lon="-117.133162")
        import_stop_times(stop_times_txt, feed)
        stoptime = StopTime.objects.get()
        self.assertEqual(stoptime.trip, trip)
        self.assertEqual(stoptime.arrival_time, time(6))
        self.assertEqual(stoptime.departure_time, time(6))
        self.assertEqual(stoptime.stop, stop)
        self.assertEqual(stoptime.stop_sequence, 1)
        self.assertEqual(stoptime.stop_headsign, '')
        self.assertEqual(stoptime.pickup_type, '')
        self.assertEqual(stoptime.drop_off_type, '')
        self.assertEqual(stoptime.shape_dist_traveled, None)
