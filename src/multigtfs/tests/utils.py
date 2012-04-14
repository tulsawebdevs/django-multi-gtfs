import os.path
import StringIO
import urllib

from django.test import TestCase

from multigtfs.models import (
    Agency, Block, FareAttributes, FareRules, Feed, FeedInfo, Frequency,
    Route, Service, ServiceDate, Shape, Stop, StopTime, Transfer, Trip, Zone)


from multigtfs.utils import import_gtfs

# Test GTFS data downloaded from
# http://timetablepublisher.googlecode.com/files/GTFS%20Test%20Data.zip
my_dir = os.path.dirname(__file__)
fix_dir = os.path.join(my_dir, 'fixtures')
test_path = os.path.abspath(os.path.join(fix_dir, 'GTFS_Test_Data.zip'))

class ImportGTFSTest(TestCase):

    def test_import_gtfs(self):
        feed = Feed.objects.create()
        with open(test_path, 'rb') as zip_file:
            import_gtfs(zip_file, feed)
        
        self.assertEqual(Agency.objects.count(), 1)
        self.assertEqual(Block.objects.count(), 6)
        self.assertEqual(FareAttributes.objects.count(), 0)
        self.assertEqual(FareRules.objects.count(), 0)
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(FeedInfo.objects.count(), 0)
        self.assertEqual(Frequency.objects.count(), 0)
        self.assertEqual(Route.objects.count(), 5)
        self.assertEqual(Service.objects.count(), 3)
        self.assertEqual(ServiceDate.objects.count(), 1)
        self.assertEqual(Shape.objects.count(), 0)
        self.assertEqual(Stop.objects.count(), 9)
        self.assertEqual(StopTime.objects.count(), 28)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(Trip.objects.count(), 11)
        self.assertEqual(Zone.objects.count(), 0)

