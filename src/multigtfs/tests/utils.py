import os.path
import StringIO
import urllib

from django.test import TestCase

from multigtfs.models import (
    Agency, Block, FareAttributes, FareRules, Feed, FeedInfo, Frequency,
    Route, Service, ServiceDate, Shape, Stop, StopTime, Transfer, Trip, Zone)
from multigtfs.utils import import_gtfs

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
        self.assertEqual(FareAttributes.objects.count(), 0)
        self.assertEqual(FareRules.objects.count(), 0)
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(FeedInfo.objects.count(), 0)
        self.assertEqual(Frequency.objects.count(), 11)
        self.assertEqual(Route.objects.count(), 5)
        self.assertEqual(Service.objects.count(), 3)
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
        self.assertEqual(FareAttributes.objects.count(), 2)
        self.assertEqual(FareRules.objects.count(), 0)
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
