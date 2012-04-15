from datetime import time
import os.path
import StringIO
import urllib

from django.test import TestCase

from multigtfs.models import (
    Agency, Block, Fare, FareRule, Feed, FeedInfo, Frequency,
    Route, Service, ServiceDate, Shape, Stop, StopTime, Transfer, Trip, Zone)
from multigtfs.utils import import_gtfs, parse_time

my_dir = os.path.dirname(__file__)
fixtures_dir = os.path.join(my_dir, 'fixtures')

class ImportGTFSTest(TestCase):

    def test_import_gtfs_test1(self):
        '''Try importing test1.zip

        test1.zip was downloaded from
        http://timetablepublisher.googlecode.com/files/GTFS%20Test%20Data.zip
        on April 14th, 2012
        '''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test1.zip'))
        feed = Feed.objects.create()
        with open(test_path, 'rb') as zip_file:
            import_gtfs(zip_file, feed)

        self.assertEqual(Agency.objects.count(), 1)
        self.assertEqual(Block.objects.count(), 6)
        self.assertEqual(Fare.objects.count(), 0)
        self.assertEqual(FareRule.objects.count(), 0)
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(FeedInfo.objects.count(), 0)
        self.assertEqual(Frequency.objects.count(), 11)
        self.assertEqual(Route.objects.count(), 5)
        self.assertEqual(Service.objects.count(), 3)
        service_W = Service.objects.get(service_id='W')
        service_S = Service.objects.get(service_id='S')
        service_U = Service.objects.get(service_id='U')
        self.assertEqual(service_W.trip_set.count(), 9)
        self.assertEqual(service_S.trip_set.count(), 4)
        self.assertEqual(service_U.trip_set.count(), 2)
        self.assertEqual(ServiceDate.objects.count(), 1)
        self.assertEqual(Shape.objects.count(), 0)
        self.assertEqual(Stop.objects.count(), 9)
        self.assertEqual(StopTime.objects.count(), 28)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(Trip.objects.count(), 11)
        self.assertEqual(Zone.objects.count(), 0)

    def test_import_gtfs_test2(self):
        '''Try importing test2.zip

        test2.zip was downloaded from
        https://developers.google.com/transit/gtfs/examples/sample-feed.zip
        on April 14th, 2012
        '''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test2.zip'))
        feed = Feed.objects.create()
        with open(test_path, 'rb') as zip_file:
            import_gtfs(zip_file, feed)

        self.assertEqual(Agency.objects.count(), 1)
        self.assertEqual(Block.objects.count(), 2)
        self.assertEqual(Fare.objects.count(), 2)
        self.assertEqual(FareRule.objects.count(), 4)
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(FeedInfo.objects.count(), 0)
        self.assertEqual(Frequency.objects.count(), 11)
        self.assertEqual(Route.objects.count(), 5)
        self.assertEqual(Service.objects.count(), 2)
        self.assertEqual(ServiceDate.objects.count(), 1)
        self.assertEqual(Shape.objects.count(), 0)
        self.assertEqual(Stop.objects.count(), 9)
        self.assertEqual(StopTime.objects.count(), 28)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(Trip.objects.count(), 11)
        self.assertEqual(Zone.objects.count(), 0)


class ParseTimeTest(TestCase):
    def test_null(self):
        t, d = parse_time(None)
        self.assertEqual(t, None)
        self.assertEqual(d, None)

    def test_blank(self):
        t, d = parse_time('')
        self.assertEqual(t, None)
        self.assertEqual(d, None)

    def test_standard(self):
        t, d = parse_time('08:30:14')
        self.assertEqual(t, time(8,30,14))
        self.assertEqual(d, 0)

    def test_next_day(self):
        t, d = parse_time('24:30:14')
        self.assertEqual(t, time(0,30,14))
        self.assertEqual(d, 1)
