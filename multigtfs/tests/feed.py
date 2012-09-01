import os
import tempfile
import zipfile

from django.test import TestCase

from multigtfs.models import (
    Agency, Block, Fare, FareRule, Feed, FeedInfo, Frequency,
    Route, Service, ServiceDate, Shape, Stop, StopTime, Transfer, Trip, Zone)

my_dir = os.path.dirname(__file__)
fixtures_dir = os.path.join(my_dir, 'fixtures')


class FeedTest(TestCase):
    
    def setUp(self):
        self.temp_path = None

    def tearDown(self):
        if self.temp_path:
            os.unlink(self.temp_path)

    def normalize(self, feed):
        '''Normalize a feed - line seperators, etc.'''
        feed = feed.replace('\r\n','\n').strip()
        lines = feed.split('\n')
        header = lines.pop(0)
        lines.sort()
        return header + '\n' + '\n'.join(lines) + '\n'

    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(feed.id, 1)
        self.assertEqual(str(feed), '1')
        feed.name = 'Test'
        self.assertEqual(str(feed), '1 Test')

    def test_import_gtfs_test1(self):
        '''Try importing test1.zip

        test1.zip was downloaded from
        http://timetablepublisher.googlecode.com/files/GTFS%20Test%20Data.zip
        on April 14th, 2012
        '''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test1.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(test_path)
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
        feed.import_gtfs(test_path)

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

    def test_export_gtfs_test1(self):
        '''Try exporting test1.zip'''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test1.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(test_path)
        file_id, self.temp_path = tempfile.mkstemp()
        os.close(file_id)
        feed.export_gtfs(self.temp_path)
        z_in = zipfile.ZipFile(test_path, 'r')
        z_out = zipfile.ZipFile(self.temp_path, 'r')
        
        agency_in = self.normalize(z_in.read('dv/agency.txt'))
        agency_out = self.normalize(z_out.read('feed/agency.txt'))
        self.assertEqual(agency_in, agency_out)
        
        calendar_in = self.normalize(z_in.read('dv/calendar.txt'))
        calendar_out = self.normalize(z_out.read('feed/calendar.txt'))
        self.assertEqual(calendar_in, calendar_out)
        
        cdates_in = self.normalize(z_in.read('dv/calendar_dates.txt'))
        cdates_out = self.normalize(z_out.read('feed/calendar_dates.txt'))
        self.assertEqual(cdates_in, cdates_out)

        self.assertTrue('dv/fare_attributes.txt' not in z_in.namelist())
        self.assertTrue('feed/fare_attributes.txt' not in z_out.namelist())

    def test_export_gtfs_test2(self):
        '''Try exporting test2.zip'''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test2.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(test_path)
        file_id, self.temp_path = tempfile.mkstemp()
        os.close(file_id)
        feed.export_gtfs(self.temp_path)
        z_in = zipfile.ZipFile(test_path, 'r')
        z_out = zipfile.ZipFile(self.temp_path, 'r')
        
        agency_in = self.normalize(z_in.read('agency.txt'))
        agency_out = self.normalize(z_out.read('feed/agency.txt'))
        self.assertEqual(agency_in, agency_out)
        
        calendar_in = self.normalize(z_in.read('calendar.txt'))
        calendar_out = self.normalize(z_out.read('feed/calendar.txt'))
        self.assertEqual(calendar_in, calendar_out)

        cdates_in = self.normalize(z_in.read('calendar_dates.txt'))
        cdates_out = self.normalize(z_out.read('feed/calendar_dates.txt'))
        self.assertEqual(cdates_in, cdates_out)

        # source fare_attributes.txt has unneeded transfer_duration column
        fare_in = self.normalize(z_in.read('fare_attributes.txt'))
        self.assertEqual(fare_in, '''\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
a,5.25,USD,0,0,
p,1.25,USD,0,0,
''')
        fare_out = z_out.read('feed/fare_attributes.txt')
        self.assertEqual(fare_out, '''\
fare_id,price,currency_type,payment_method,transfers
a,5.25,USD,0,0
p,1.25,USD,0,0
''')
