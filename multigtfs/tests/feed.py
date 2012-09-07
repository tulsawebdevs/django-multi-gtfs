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
        feed = feed.replace('\r\n', '\n').strip()
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

        self.assertFalse('dv/fare_attributes.txt' in z_in.namelist())
        self.assertFalse('feed/fare_attributes.txt' in z_out.namelist())

        self.assertFalse('dv/fare_rules.txt' in z_in.namelist())
        self.assertFalse('feed/fare_rules.txt' in z_out.namelist())

        self.assertFalse('dv/feed_info.txt' in z_in.namelist())
        self.assertFalse('feed/feed_info.txt' in z_out.namelist())

        freq_in = self.normalize(z_in.read('dv/frequencies.txt'))
        self.assertEqual(freq_in, '''\
trip_id,start_time,end_time,headway_secs
CITY1,10:00:00,15:59:59,1800
CITY1,16:00:00,18:59:59,600
CITY1,19:00:00,22:00:00,1800
CITY1,6:00:00,7:59:59,1800
CITY1,8:00:00,9:59:59,600
CITY2,10:00:00,15:59:59,1800
CITY2,16:00:00,18:59:59,600
CITY2,19:00:00,22:00:00,1800
CITY2,6:00:00,7:59:59,1800
CITY2,8:00:00,9:59:59,600
STBA,6:00:00,22:00:00,1800
''')
        freq_out = self.normalize(z_out.read('feed/frequencies.txt'))
        self.assertNotEqual(freq_out, "Le Freak, C'est Chic")
        self.assertEqual(freq_out, '''\
trip_id,start_time,end_time,headway_secs
CITY1,06:00:00,07:59:59,1800
CITY1,08:00:00,09:59:59,600
CITY1,10:00:00,15:59:59,1800
CITY1,16:00:00,18:59:59,600
CITY1,19:00:00,22:00:00,1800
CITY2,06:00:00,07:59:59,1800
CITY2,08:00:00,09:59:59,600
CITY2,10:00:00,15:59:59,1800
CITY2,16:00:00,18:59:59,600
CITY2,19:00:00,22:00:00,1800
STBA,06:00:00,22:00:00,1800
''')

        routes_in = self.normalize(z_in.read('dv/routes.txt'))
        routes_out = self.normalize(z_out.read('feed/routes.txt'))
        self.assertEqual(routes_in, routes_out)

        self.assertFalse('dv/shapes.txt' in z_in.namelist())
        self.assertFalse('feed/shapes.txt' in z_out.namelist())

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

        # source fare_rules.txt has unneeded columns
        fare_rules_in = self.normalize(z_in.read('fare_rules.txt'))
        self.assertEqual(fare_rules_in, '''\
fare_id,route_id,origin_id,destination_id,contains_id
a,AAMV,,,
p,AB,,,
p,BFC,,,
p,STBA,,,
''')
        fare_rules_out = self.normalize(z_out.read('feed/fare_rules.txt'))
        self.assertEqual(fare_rules_out, '''\
fare_id,route_id
a,AAMV
p,AB
p,BFC
p,STBA
''')

        self.assertFalse('feed_info.txt' in z_in.namelist())
        self.assertFalse('feed/feed_info.txt' in z_out.namelist())

        freq_in = self.normalize(z_in.read('frequencies.txt'))
        self.assertEqual(freq_in, '''\
trip_id,start_time,end_time,headway_secs
CITY1,10:00:00,15:59:59,1800
CITY1,16:00:00,18:59:59,600
CITY1,19:00:00,22:00:00,1800
CITY1,6:00:00,7:59:59,1800
CITY1,8:00:00,9:59:59,600
CITY2,10:00:00,15:59:59,1800
CITY2,16:00:00,18:59:59,600
CITY2,19:00:00,22:00:00,1800
CITY2,6:00:00,7:59:59,1800
CITY2,8:00:00,9:59:59,600
STBA,6:00:00,22:00:00,1800
''')
        freq_out = self.normalize(z_out.read('feed/frequencies.txt'))
        self.assertEqual(freq_out, '''\
trip_id,start_time,end_time,headway_secs
CITY1,06:00:00,07:59:59,1800
CITY1,08:00:00,09:59:59,600
CITY1,10:00:00,15:59:59,1800
CITY1,16:00:00,18:59:59,600
CITY1,19:00:00,22:00:00,1800
CITY2,06:00:00,07:59:59,1800
CITY2,08:00:00,09:59:59,600
CITY2,10:00:00,15:59:59,1800
CITY2,16:00:00,18:59:59,600
CITY2,19:00:00,22:00:00,1800
STBA,06:00:00,22:00:00,1800
''')

        routes_in = self.normalize(z_in.read('routes.txt'))
        self.assertEqual(routes_in, """\
route_id,agency_id,route_short_name,route_long_name,route_desc,route_type\
,route_url,route_color,route_text_color
AAMV,DTA,50,Airport - Amargosa Valley,,3,,,
AB,DTA,10,Airport - Bullfrog,,3,,,
BFC,DTA,20,Bullfrog - Furnace Creek Resort,,3,,,
CITY,DTA,40,City,,3,,,
STBA,DTA,30,Stagecoach - Airport Shuttle,,3,,,
""")
        routes_out = self.normalize(z_out.read('feed/routes.txt'))
        self.assertEqual(routes_out, """\
route_id,agency_id,route_short_name,route_long_name,route_type
AAMV,DTA,50,Airport - Amargosa Valley,3
AB,DTA,10,Airport - Bullfrog,3
BFC,DTA,20,Bullfrog - Furnace Creek Resort,3
CITY,DTA,40,City,3
STBA,DTA,30,Stagecoach - Airport Shuttle,3
""")

        shapes_out = self.normalize(z_in.read('shapes.txt'))
        self.assertEqual(shapes_out, '''\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled

''')
        self.assertFalse('feed/shapes.txt' in z_out.namelist())
