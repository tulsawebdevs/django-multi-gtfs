from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Block, Calendar, Feed, Route, Shape, Trip
from multigtfs.utils import import_trips


class TripModelTest(TestCase):
    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(feed.id, 1)
        route = Route.objects.create(feed=feed, route_id='R1', rtype=3)
        trip = Trip.objects.create(route=route, trip_id='T1')
        self.assertEqual(str(trip), '1-R1-T1')


class ImportTripsTest(TestCase):

    def test_import_trips_minimal(self):
        trips_txt = StringIO.StringIO("""\
route_id,service_id,trip_id
R1,S1,T1
""")
        feed = Feed.objects.create()
        route = Route.objects.create(feed=feed, route_id='R1', rtype=3)
        service = Calendar.objects.create(
            feed=feed, service_id='S1', start_date=date(2011,4,14), 
            end_date=date(2011,12,31))
        
        import_trips(trips_txt, feed)
        trip = Trip.objects.get()
        self.assertEqual(trip.feed, feed)
        self.assertEqual(trip.route, route)
        self.assertEqual(trip.service, service)
        self.assertEqual(trip.trip_id, 'T1')
        self.assertEqual(trip.headsign, '')
        self.assertEqual(trip.short_name, '')
        self.assertEqual(trip.direction, '')
        self.assertEqual(trip.block, None)
        self.assertEqual(trip.shape, None)

    def test_import_trips_maximal(self):
        trips_txt = StringIO.StringIO("""\
route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,\
block_id,shape_id
R1,S1,T1,Headsign,HS,0,B1,S1
""")
        feed = Feed.objects.create()
        route = Route.objects.create(feed=feed, route_id='R1', rtype=3)
        service = Calendar.objects.create(
            feed=feed, service_id='S1', start_date=date(2011,4,14), 
            end_date=date(2011,12,31))
        block = Block.objects.create(feed=feed, block_id='B1')
        shape = Shape.objects.create(feed=feed, shape_id='S1')
        import_trips(trips_txt, feed)
        trip = Trip.objects.get()
        self.assertEqual(trip.feed, feed)
        self.assertEqual(trip.route, route)
        self.assertEqual(trip.service, service)
        self.assertEqual(trip.trip_id, 'T1')
        self.assertEqual(trip.headsign, 'Headsign')
        self.assertEqual(trip.short_name, 'HS')
        self.assertEqual(trip.direction, '0')
        self.assertEqual(trip.block, block)
        self.assertEqual(trip.shape, shape)
