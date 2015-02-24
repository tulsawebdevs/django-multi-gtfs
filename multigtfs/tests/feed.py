#
# Copyright 2012-2014 John Whitlock
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

from __future__ import unicode_literals

import os
import shutil
import tempfile
import zipfile

from django.test import TestCase
from django.utils.six import text_type

from multigtfs.models import (
    Agency, Block, Fare, FareRule, Feed, FeedInfo, Frequency,
    Route, Service, ServiceDate, Shape, ShapePoint, Stop, StopTime, Transfer,
    Trip, Zone)

my_dir = os.path.dirname(__file__)
fixtures_dir = os.path.join(my_dir, 'fixtures')


class FeedTest(TestCase):

    def setUp(self):
        self.temp_path = None
        self.temp_dir = None

    def tearDown(self):
        if self.temp_path:
            os.unlink(self.temp_path)
        if self.temp_dir:
            shutil.rmtree(self.temp_dir)

    def normalize(self, feed):
        '''Normalize a feed - line seperators, etc.'''
        feed = feed.replace(b'\r\n', b'\n').strip()
        lines = feed.split(b'\n')
        header = lines.pop(0)
        lines.sort()
        return header + b'\n' + b'\n'.join(lines) + b'\n'

    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(str(feed), '%d' % feed.id)
        feed.name = 'Test'
        self.assertEqual(str(feed), '%d Test' % feed.id)

    def test_import_gtfs_test1(self, gtfs_obj=None):
        '''Try importing test1.zip

        test1.zip was downloaded from
        http://timetablepublisher.googlecode.com/files/GTFS%20Test%20Data.zip
        on April 14th, 2012

        dv/trips.txt contains multiple lines with trip id BFC1 and BFC2:

        BFC,W,BFC1,to Furnace Creek Resort,0,1
        BFC,W,BFC2,to Bullfrog,1,2
        BFC,S,BFC1,to Furnace Creek Resort,0,1
        BFC,S,BFC2,to Bullfrog,1,2
        BFC,U,BFC1,to Furnace Creek Resort,0,1
        BFC,U,BFC2,to Bullfrog,1,2

        Before 0.4.0, these were imported with a many-to-many relation to
        services table.  After 0.4.0, the service ID was changed to a single
        foriegn key, so only the 'W' service is recorded.
        '''
        gtfs_obj = gtfs_obj or os.path.abspath(
            os.path.join(fixtures_dir, 'test1.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(gtfs_obj)
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
        self.assertEqual(service_S.trip_set.count(), 2)  # 2 trips dropped
        self.assertEqual(service_U.trip_set.count(), 0)  # 2 trips dropped
        self.assertEqual(ServiceDate.objects.count(), 1)
        self.assertEqual(Shape.objects.count(), 0)
        self.assertEqual(Stop.objects.count(), 9)
        self.assertEqual(StopTime.objects.count(), 28)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(Trip.objects.count(), 11)
        self.assertEqual(Zone.objects.count(), 0)

    def test_import_gtfs_test1_extracted(self):
        '''Import test1.zip as an extracted folder'''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test1.zip'))
        self.temp_dir = tempfile.mkdtemp()
        z = zipfile.ZipFile(test_path)
        z.extractall(self.temp_dir)
        self.test_import_gtfs_test1(self.temp_dir)

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

    def test_import_gtfs_test3(self):
        '''Try importing test3.zip

        test3.zip is a version of the GTFS feed from
        http://www.tulsatransit.org/gtfs/google_transit.zip
        as it was around February 2013.  It has been reduced to one route,
        trip, and shape, along with associated stops and other records.
        '''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test3.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(test_path)
        self.assertEqual(Agency.objects.count(), 1)
        self.assertEqual(Block.objects.count(), 0)
        self.assertEqual(Fare.objects.count(), 1)
        self.assertEqual(FareRule.objects.count(), 1)
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(FeedInfo.objects.count(), 1)
        self.assertEqual(Frequency.objects.count(), 0)
        self.assertEqual(Route.objects.count(), 1)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(ServiceDate.objects.count(), 7)
        self.assertEqual(Shape.objects.count(), 1)
        self.assertEqual(ShapePoint.objects.count(), 61)
        self.assertEqual(Stop.objects.count(), 24)
        self.assertEqual(StopTime.objects.count(), 25)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(Zone.objects.count(), 0)

    def test_import_gtfs_test4(self):
        '''Try importing test4.zip

        test4.zip is a version of the GTFS feed from TriMet in Portland
        from February 2015.  It omits calendar.txt in favor of specifying
        all dates in calendar_dates.txt, and includes additional files not
        in the GTFS spec.
        '''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test4.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(test_path)
        self.assertEqual(Agency.objects.count(), 1)
        self.assertEqual(Block.objects.count(), 1)
        self.assertEqual(Fare.objects.count(), 1)
        self.assertEqual(FareRule.objects.count(), 1)
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(FeedInfo.objects.count(), 1)
        self.assertEqual(Frequency.objects.count(), 0)
        self.assertEqual(Route.objects.count(), 1)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(ServiceDate.objects.count(), 15)
        self.assertEqual(Shape.objects.count(), 1)
        self.assertEqual(ShapePoint.objects.count(), 131)
        self.assertEqual(Stop.objects.count(), 10)
        self.assertEqual(StopTime.objects.count(), 10)
        self.assertEqual(Transfer.objects.count(), 2)
        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(Zone.objects.count(), 1)

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
        self.assertEqual(
            z_in.namelist(),
            ['dv/', 'dv/.DS_Store', '__MACOSX/', '__MACOSX/dv/',
             '__MACOSX/dv/._.DS_Store',
             'dv/agency.txt',
             'dv/calendar.txt',
             'dv/calendar_dates.txt',
             'dv/frequencies.txt',
             'dv/routes.txt',
             'dv/stop_times.txt',
             'dv/stops.txt',
             'dv/trips.txt'])
        self.assertEqual(
            z_out.namelist(),
            ['agency.txt',
             'calendar.txt',
             'calendar_dates.txt',
             'frequencies.txt',
             'routes.txt',
             'stop_times.txt',
             'stops.txt',
             'trips.txt'])

        agency_in = self.normalize(z_in.read('dv/agency.txt'))
        agency_out = self.normalize(z_out.read('agency.txt'))
        self.assertEqual(agency_in, agency_out)

        calendar_in = self.normalize(z_in.read('dv/calendar.txt'))
        calendar_out = self.normalize(z_out.read('calendar.txt'))
        self.assertEqual(calendar_in, calendar_out)

        cdates_in = self.normalize(z_in.read('dv/calendar_dates.txt'))
        cdates_out = self.normalize(z_out.read('calendar_dates.txt'))
        self.assertEqual(cdates_in, cdates_out)

        self.assertFalse('dv/fare_attributes.txt' in z_in.namelist())
        self.assertFalse('feed/fare_attributes.txt' in z_out.namelist())

        self.assertFalse('dv/fare_rules.txt' in z_in.namelist())
        self.assertFalse('feed/fare_rules.txt' in z_out.namelist())

        self.assertFalse('dv/feed_info.txt' in z_in.namelist())
        self.assertFalse('feed/feed_info.txt' in z_out.namelist())

        freq_in = self.normalize(z_in.read('dv/frequencies.txt'))
        self.assertEqual(freq_in, b'''\
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
        freq_out = self.normalize(z_out.read('frequencies.txt'))
        self.assertNotEqual(freq_out, "Le Freak, C'est Chic")
        self.assertEqual(freq_out, b'''\
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
        routes_out = self.normalize(z_out.read('routes.txt'))
        self.assertEqual(routes_in, routes_out)

        self.assertFalse('dv/shapes.txt' in z_in.namelist())
        self.assertFalse('feed/shapes.txt' in z_out.namelist())

        stimes_in = self.normalize(z_in.read('dv/stop_times.txt'))
        self.assertEqual(stimes_in, b"""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
AAMV1,8:00:00,8:00:00,BEATTY_AIRPORT,1
AAMV1,9:00:00,9:00:00,AMV,2
AAMV2,10:00:00,10:00:00,AMV,1
AAMV2,11:00:00,11:00:00,BEATTY_AIRPORT,2
AAMV3,13:00:00,13:00:00,BEATTY_AIRPORT,1
AAMV3,14:00:00,14:00:00,AMV,2
AAMV4,15:00:00,15:00:00,AMV,1
AAMV4,16:00:00,16:00:00,BEATTY_AIRPORT,2
AB1,8:00:00,8:00:00,BEATTY_AIRPORT,1
AB1,8:10:00,8:15:00,BULLFROG,2
AB2,12:05:00,12:05:00,BULLFROG,1
AB2,12:15:00,12:15:00,BEATTY_AIRPORT,2
BFC1,8:20:00,8:20:00,BULLFROG,1
BFC1,9:20:00,9:20:00,FUR_CREEK_RES,2
BFC2,11:00:00,11:00:00,FUR_CREEK_RES,1
BFC2,12:00:00,12:00:00,BULLFROG,2
CITY1,6:00:00,6:00:00,STAGECOACH,1
CITY1,6:05:00,6:07:00,NANAA,2
CITY1,6:12:00,6:14:00,NADAV,3
CITY1,6:19:00,6:21:00,DADAN,4
CITY1,6:26:00,6:28:00,EMSI,5
CITY2,6:28:00,6:30:00,EMSI,1
CITY2,6:35:00,6:37:00,DADAN,2
CITY2,6:42:00,6:44:00,NADAV,3
CITY2,6:49:00,6:51:00,NANAA,4
CITY2,6:56:00,6:58:00,STAGECOACH,5
STBA,6:00:00,6:00:00,STAGECOACH,1
STBA,6:20:00,6:20:00,BEATTY_AIRPORT,2
""")
        stimes_out = self.normalize(z_out.read('stop_times.txt'))
        self.assertEqual(stimes_out, b"""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
AAMV1,08:00:00,08:00:00,BEATTY_AIRPORT,1
AAMV1,09:00:00,09:00:00,AMV,2
AAMV2,10:00:00,10:00:00,AMV,1
AAMV2,11:00:00,11:00:00,BEATTY_AIRPORT,2
AAMV3,13:00:00,13:00:00,BEATTY_AIRPORT,1
AAMV3,14:00:00,14:00:00,AMV,2
AAMV4,15:00:00,15:00:00,AMV,1
AAMV4,16:00:00,16:00:00,BEATTY_AIRPORT,2
AB1,08:00:00,08:00:00,BEATTY_AIRPORT,1
AB1,08:10:00,08:15:00,BULLFROG,2
AB2,12:05:00,12:05:00,BULLFROG,1
AB2,12:15:00,12:15:00,BEATTY_AIRPORT,2
BFC1,08:20:00,08:20:00,BULLFROG,1
BFC1,09:20:00,09:20:00,FUR_CREEK_RES,2
BFC2,11:00:00,11:00:00,FUR_CREEK_RES,1
BFC2,12:00:00,12:00:00,BULLFROG,2
CITY1,06:00:00,06:00:00,STAGECOACH,1
CITY1,06:05:00,06:07:00,NANAA,2
CITY1,06:12:00,06:14:00,NADAV,3
CITY1,06:19:00,06:21:00,DADAN,4
CITY1,06:26:00,06:28:00,EMSI,5
CITY2,06:28:00,06:30:00,EMSI,1
CITY2,06:35:00,06:37:00,DADAN,2
CITY2,06:42:00,06:44:00,NADAV,3
CITY2,06:49:00,06:51:00,NANAA,4
CITY2,06:56:00,06:58:00,STAGECOACH,5
STBA,06:00:00,06:00:00,STAGECOACH,1
STBA,06:20:00,06:20:00,BEATTY_AIRPORT,2
""")

        stops_in = self.normalize(z_in.read('dv/stops.txt'))
        self.assertEqual(stops_in, b"""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon
AMV,Amargosa Valley (Demo),,36.641496,-116.40094
BEATTY_AIRPORT,Nye County Airport (Demo),,36.868446,-116.784582
BULLFROG,Bullfrog (Demo),,36.88108,-116.81797
DADAN,Doing Ave / D Ave N (Demo),,36.909489,-116.768242
EMSI,E Main St / S Irving St (Demo),,36.905697,-116.76218
FUR_CREEK_RES,Furnace Creek Resort (Demo),,36.425288,-117.133162
NADAV,North Ave / D Ave N (Demo),,36.914893,-116.76821
NANAA,North Ave / N A Ave (Demo),,36.914944,-116.761472
STAGECOACH,Stagecoach Hotel & Casino (Demo),,36.915682,-116.751677
""")
        stops_out = self.normalize(z_out.read('stops.txt'))
        self.assertEqual(stops_out, b"""\
stop_id,stop_name,stop_lat,stop_lon
AMV,Amargosa Valley (Demo),36.641496,-116.40094
BEATTY_AIRPORT,Nye County Airport (Demo),36.868446,-116.784582
BULLFROG,Bullfrog (Demo),36.88108,-116.81797
DADAN,Doing Ave / D Ave N (Demo),36.909489,-116.768242
EMSI,E Main St / S Irving St (Demo),36.905697,-116.76218
FUR_CREEK_RES,Furnace Creek Resort (Demo),36.425288,-117.133162
NADAV,North Ave / D Ave N (Demo),36.914893,-116.76821
NANAA,North Ave / N A Ave (Demo),36.914944,-116.761472
STAGECOACH,Stagecoach Hotel & Casino (Demo),36.915682,-116.751677
""")

        self.assertFalse('dv/transfers.txt' in z_in.namelist())
        self.assertFalse('feed/transfers.txt' in z_out.namelist())

        # Duplicate trips are dropped
        trips_out = self.normalize(z_out.read('trips.txt'))
        self.assertEqual(trips_out, b"""\
route_id,service_id,trip_id,trip_headsign,direction_id,block_id
AAMV,S,AAMV3,to Amargosa Valley,0,4
AAMV,S,AAMV4,to Airport,1,4
AAMV,W,AAMV1,to Amargosa Valley,0,3
AAMV,W,AAMV2,to Airport,1,3
AB,W,AB1,to Bullfrog,0,1
AB,W,AB2,to Airport,1,2
BFC,W,BFC1,to Furnace Creek Resort,0,1
BFC,W,BFC2,to Bullfrog,1,2
CITY,W,CITY1,to Somewhere,0,44
CITY,W,CITY2,to Nowhere,1,45
STBA,W,STBA,Shuttle,1,2
""")

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

        self.assertEqual(
            z_in.namelist(),
            ['agency.txt',
             'calendar.txt',
             'calendar_dates.txt',
             'fare_attributes.txt',
             'fare_rules.txt',
             'frequencies.txt',
             'routes.txt',
             'shapes.txt',
             'stop_times.txt',
             'stops.txt',
             'trips.txt'])
        self.assertEqual(
            z_out.namelist(),
            ['agency.txt',
             'calendar.txt',
             'calendar_dates.txt',
             'fare_attributes.txt',
             'fare_rules.txt',
             'frequencies.txt',
             'routes.txt',
             'stop_times.txt',
             'stops.txt',
             'trips.txt'])

        agency_in = self.normalize(z_in.read('agency.txt'))
        agency_out = self.normalize(z_out.read('agency.txt'))
        self.assertEqual(agency_in, agency_out)

        calendar_in = self.normalize(z_in.read('calendar.txt'))
        calendar_out = self.normalize(z_out.read('calendar.txt'))
        self.assertEqual(calendar_in, calendar_out)

        cdates_in = self.normalize(z_in.read('calendar_dates.txt'))
        cdates_out = self.normalize(z_out.read('calendar_dates.txt'))
        self.assertEqual(cdates_in, cdates_out)

        # source fare_attributes.txt has unneeded transfer_duration column
        fare_in = self.normalize(z_in.read('fare_attributes.txt'))
        self.assertEqual(fare_in, b'''\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
a,5.25,USD,0,0,
p,1.25,USD,0,0,
''')
        # Sometimes 5.2500, sometimes 5.25
        fare_a = Fare.objects.get(fare_id='a')
        fare_p = Fare.objects.get(fare_id='p')
        s_fare_a = text_type(fare_a.price).encode('utf-8')
        s_fare_p = text_type(fare_p.price).encode('utf-8')
        fare_out = z_out.read('fare_attributes.txt')
        self.assertEqual(fare_out, b'''\
fare_id,price,currency_type,payment_method,transfers
a,''' + s_fare_a + b''',USD,0,0
p,''' + s_fare_p + b''',USD,0,0
''')

        # source fare_rules.txt has unneeded columns
        fare_rules_in = self.normalize(z_in.read('fare_rules.txt'))
        self.assertEqual(fare_rules_in, b'''\
fare_id,route_id,origin_id,destination_id,contains_id
a,AAMV,,,
p,AB,,,
p,BFC,,,
p,STBA,,,
''')
        fare_rules_out = self.normalize(z_out.read('fare_rules.txt'))
        self.assertEqual(fare_rules_out, b'''\
fare_id,route_id
a,AAMV
p,AB
p,BFC
p,STBA
''')

        self.assertFalse('feed_info.txt' in z_in.namelist())
        self.assertFalse('feed/feed_info.txt' in z_out.namelist())

        freq_in = self.normalize(z_in.read('frequencies.txt'))
        self.assertEqual(freq_in, b'''\
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
        freq_out = self.normalize(z_out.read('frequencies.txt'))
        self.assertEqual(freq_out, b'''\
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
        self.assertEqual(routes_in, b"""\
route_id,agency_id,route_short_name,route_long_name,route_desc,route_type\
,route_url,route_color,route_text_color
AAMV,DTA,50,Airport - Amargosa Valley,,3,,,
AB,DTA,10,Airport - Bullfrog,,3,,,
BFC,DTA,20,Bullfrog - Furnace Creek Resort,,3,,,
CITY,DTA,40,City,,3,,,
STBA,DTA,30,Stagecoach - Airport Shuttle,,3,,,
""")
        routes_out = self.normalize(z_out.read('routes.txt'))
        self.assertEqual(routes_out, b"""\
route_id,agency_id,route_short_name,route_long_name,route_type
AAMV,DTA,50,Airport - Amargosa Valley,3
AB,DTA,10,Airport - Bullfrog,3
BFC,DTA,20,Bullfrog - Furnace Creek Resort,3
CITY,DTA,40,City,3
STBA,DTA,30,Stagecoach - Airport Shuttle,3
""")

        shapes_out = self.normalize(z_in.read('shapes.txt'))
        self.assertEqual(shapes_out, b'''\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled

''')
        self.assertFalse('feed/shapes.txt' in z_out.namelist())

        stimes_in = self.normalize(z_in.read('stop_times.txt'))
        self.assertEqual(stimes_in, b"""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,\
pickup_type,drop_off_time,shape_dist_traveled
AAMV1,8:00:00,8:00:00,BEATTY_AIRPORT,1
AAMV1,9:00:00,9:00:00,AMV,2
AAMV2,10:00:00,10:00:00,AMV,1
AAMV2,11:00:00,11:00:00,BEATTY_AIRPORT,2
AAMV3,13:00:00,13:00:00,BEATTY_AIRPORT,1
AAMV3,14:00:00,14:00:00,AMV,2
AAMV4,15:00:00,15:00:00,AMV,1
AAMV4,16:00:00,16:00:00,BEATTY_AIRPORT,2
AB1,8:00:00,8:00:00,BEATTY_AIRPORT,1,,,,
AB1,8:10:00,8:15:00,BULLFROG,2,,,,
AB2,12:05:00,12:05:00,BULLFROG,1,,,,
AB2,12:15:00,12:15:00,BEATTY_AIRPORT,2
BFC1,8:20:00,8:20:00,BULLFROG,1
BFC1,9:20:00,9:20:00,FUR_CREEK_RES,2
BFC2,11:00:00,11:00:00,FUR_CREEK_RES,1
BFC2,12:00:00,12:00:00,BULLFROG,2
CITY1,6:00:00,6:00:00,STAGECOACH,1,,,,
CITY1,6:05:00,6:07:00,NANAA,2,,,,
CITY1,6:12:00,6:14:00,NADAV,3,,,,
CITY1,6:19:00,6:21:00,DADAN,4,,,,
CITY1,6:26:00,6:28:00,EMSI,5,,,,
CITY2,6:28:00,6:30:00,EMSI,1,,,,
CITY2,6:35:00,6:37:00,DADAN,2,,,,
CITY2,6:42:00,6:44:00,NADAV,3,,,,
CITY2,6:49:00,6:51:00,NANAA,4,,,,
CITY2,6:56:00,6:58:00,STAGECOACH,5,,,,
STBA,6:00:00,6:00:00,STAGECOACH,1,,,,
STBA,6:20:00,6:20:00,BEATTY_AIRPORT,2,,,,
""")
        stimes_out = self.normalize(z_out.read('stop_times.txt'))
        self.assertEqual(stimes_out, b"""\
trip_id,arrival_time,departure_time,stop_id,stop_sequence
AAMV1,08:00:00,08:00:00,BEATTY_AIRPORT,1
AAMV1,09:00:00,09:00:00,AMV,2
AAMV2,10:00:00,10:00:00,AMV,1
AAMV2,11:00:00,11:00:00,BEATTY_AIRPORT,2
AAMV3,13:00:00,13:00:00,BEATTY_AIRPORT,1
AAMV3,14:00:00,14:00:00,AMV,2
AAMV4,15:00:00,15:00:00,AMV,1
AAMV4,16:00:00,16:00:00,BEATTY_AIRPORT,2
AB1,08:00:00,08:00:00,BEATTY_AIRPORT,1
AB1,08:10:00,08:15:00,BULLFROG,2
AB2,12:05:00,12:05:00,BULLFROG,1
AB2,12:15:00,12:15:00,BEATTY_AIRPORT,2
BFC1,08:20:00,08:20:00,BULLFROG,1
BFC1,09:20:00,09:20:00,FUR_CREEK_RES,2
BFC2,11:00:00,11:00:00,FUR_CREEK_RES,1
BFC2,12:00:00,12:00:00,BULLFROG,2
CITY1,06:00:00,06:00:00,STAGECOACH,1
CITY1,06:05:00,06:07:00,NANAA,2
CITY1,06:12:00,06:14:00,NADAV,3
CITY1,06:19:00,06:21:00,DADAN,4
CITY1,06:26:00,06:28:00,EMSI,5
CITY2,06:28:00,06:30:00,EMSI,1
CITY2,06:35:00,06:37:00,DADAN,2
CITY2,06:42:00,06:44:00,NADAV,3
CITY2,06:49:00,06:51:00,NANAA,4
CITY2,06:56:00,06:58:00,STAGECOACH,5
STBA,06:00:00,06:00:00,STAGECOACH,1
STBA,06:20:00,06:20:00,BEATTY_AIRPORT,2
""")

        stops_in = self.normalize(z_in.read('stops.txt'))
        self.assertEqual(stops_in, b"""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url
AMV,Amargosa Valley (Demo),,36.641496,-116.40094,,
BEATTY_AIRPORT,Nye County Airport (Demo),,36.868446,-116.784582,,
BULLFROG,Bullfrog (Demo),,36.88108,-116.81797,,
DADAN,Doing Ave / D Ave N (Demo),,36.909489,-116.768242,,
EMSI,E Main St / S Irving St (Demo),,36.905697,-116.76218,,
FUR_CREEK_RES,Furnace Creek Resort (Demo),,36.425288,-117.133162,,
NADAV,North Ave / D Ave N (Demo),,36.914893,-116.76821,,
NANAA,North Ave / N A Ave (Demo),,36.914944,-116.761472,,
STAGECOACH,Stagecoach Hotel & Casino (Demo),,36.915682,-116.751677,,
""")
        stops_out = self.normalize(z_out.read('stops.txt'))
        self.assertEqual(stops_out, b"""\
stop_id,stop_name,stop_lat,stop_lon
AMV,Amargosa Valley (Demo),36.641496,-116.40094
BEATTY_AIRPORT,Nye County Airport (Demo),36.868446,-116.784582
BULLFROG,Bullfrog (Demo),36.88108,-116.81797
DADAN,Doing Ave / D Ave N (Demo),36.909489,-116.768242
EMSI,E Main St / S Irving St (Demo),36.905697,-116.76218
FUR_CREEK_RES,Furnace Creek Resort (Demo),36.425288,-117.133162
NADAV,North Ave / D Ave N (Demo),36.914893,-116.76821
NANAA,North Ave / N A Ave (Demo),36.914944,-116.761472
STAGECOACH,Stagecoach Hotel & Casino (Demo),36.915682,-116.751677
""")

        self.assertFalse('transfers.txt' in z_in.namelist())
        self.assertFalse('feed/transfers.txt' in z_out.namelist())

        trips_in = self.normalize(z_in.read('trips.txt'))
        self.assertEqual(trips_in, b"""\
route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id
AAMV,WE,AAMV1,to Amargosa Valley,0,,
AAMV,WE,AAMV2,to Airport,1,,
AAMV,WE,AAMV3,to Amargosa Valley,0,,
AAMV,WE,AAMV4,to Airport,1,,
AB,FULLW,AB1,to Bullfrog,0,1,
AB,FULLW,AB2,to Airport,1,2,
BFC,FULLW,BFC1,to Furnace Creek Resort,0,1,
BFC,FULLW,BFC2,to Bullfrog,1,2,
CITY,FULLW,CITY1,,0,,
CITY,FULLW,CITY2,,1,,
STBA,FULLW,STBA,Shuttle,,,
""")
        trips_out = self.normalize(z_out.read('trips.txt'))
        self.assertEqual(trips_out, b"""\
route_id,service_id,trip_id,trip_headsign,direction_id,block_id
AAMV,WE,AAMV1,to Amargosa Valley,0,
AAMV,WE,AAMV2,to Airport,1,
AAMV,WE,AAMV3,to Amargosa Valley,0,
AAMV,WE,AAMV4,to Airport,1,
AB,FULLW,AB1,to Bullfrog,0,1
AB,FULLW,AB2,to Airport,1,2
BFC,FULLW,BFC1,to Furnace Creek Resort,0,1
BFC,FULLW,BFC2,to Bullfrog,1,2
CITY,FULLW,CITY1,,0,
CITY,FULLW,CITY2,,1,
STBA,FULLW,STBA,Shuttle,,
""")

    def test_export_gtfs_test3(self):
        '''Try exporting test3.zip'''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test3.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(test_path)
        file_id, self.temp_path = tempfile.mkstemp()
        os.close(file_id)
        feed.export_gtfs(self.temp_path)
        z_in = zipfile.ZipFile(test_path, 'r')
        z_out = zipfile.ZipFile(self.temp_path, 'r')

        self.assertEqual(
            z_in.namelist(),
            ['agency.txt',
             'calendar.txt',
             'calendar_dates.txt',
             'fare_attributes.txt',
             'fare_rules.txt',
             'feed_info.txt',
             'routes.txt',
             'shapes.txt',
             'stop_times.txt',
             'stops.txt',
             'trips.txt'])
        self.assertEqual(
            z_out.namelist(),
            ['agency.txt',
             'calendar.txt',
             'calendar_dates.txt',
             'fare_attributes.txt',
             'fare_rules.txt',
             'feed_info.txt',
             'routes.txt',
             'shapes.txt',
             'stop_times.txt',
             'stops.txt',
             'trips.txt'])

        agency_in = self.normalize(z_in.read('agency.txt'))
        agency_out = self.normalize(z_out.read('agency.txt'))
        self.assertEqual(agency_in, agency_out)

        calendar_in = self.normalize(z_in.read('calendar.txt'))
        calendar_out = self.normalize(z_out.read('calendar.txt'))
        self.assertEqual(calendar_in, calendar_out)

        cdates_in = self.normalize(z_in.read('calendar_dates.txt'))
        cdates_out = self.normalize(z_out.read('calendar_dates.txt'))
        self.assertEqual(cdates_in, cdates_out)

        fare_in = self.normalize(z_in.read('fare_attributes.txt'))
        self.assertEqual(fare_in, b'''\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
adult,1.5000,USD,0,,7200
''')
        # Sometimes 1.5000, sometimes 1.5
        fare_a = Fare.objects.get(fare_id='adult')
        s_fare_a = text_type(fare_a.price).encode('utf-8')
        fare_out = z_out.read('fare_attributes.txt')
        self.assertEqual(fare_out, b'''\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
adult,''' + s_fare_a + b''',USD,0,,7200
''')

        fare_rules_in = self.normalize(z_in.read('fare_rules.txt'))
        fare_rules_out = self.normalize(z_out.read('fare_rules.txt'))
        self.assertEqual(fare_rules_in, fare_rules_out)

        feed_info_in = self.normalize(z_in.read('feed_info.txt'))
        feed_info_out = self.normalize(z_out.read('feed_info.txt'))
        self.assertEqual(feed_info_in, feed_info_out)

        self.assertFalse('frequencies.txt' in z_in.namelist())
        self.assertFalse('frequencies.txt' in z_out.namelist())

        routes_in = self.normalize(z_in.read('routes.txt'))
        routes_out = self.normalize(z_out.read('routes.txt'))
        self.assertEqual(routes_in, routes_out)

        shapes_in = self.normalize(z_in.read('shapes.txt'))
        shapes_out = self.normalize(z_out.read('shapes.txt'))
        self.assertEqual(shapes_in, shapes_out)

        stop_times_in = self.normalize(z_in.read('stop_times.txt'))
        stop_times_out = self.normalize(z_out.read('stop_times.txt'))
        self.assertEqual(stop_times_in, stop_times_out)

        stops_in = self.normalize(z_in.read('stops.txt'))
        stops_out = self.normalize(z_out.read('stops.txt'))
        self.assertEqual(stops_in, stops_out)

        self.assertFalse('transfers.txt' in z_in.namelist())
        self.assertFalse('feed/transfers.txt' in z_out.namelist())

        trips_in = self.normalize(z_in.read('trips.txt'))
        trips_out = self.normalize(z_out.read('trips.txt'))
        self.assertEqual(trips_in, trips_out)

    def test_export_gtfs_test4(self):
        '''Try exporting test4.zip'''
        test_path = os.path.abspath(os.path.join(fixtures_dir, 'test4.zip'))
        feed = Feed.objects.create()
        feed.import_gtfs(test_path)
        file_id, self.temp_path = tempfile.mkstemp()
        os.close(file_id)
        feed.export_gtfs(self.temp_path)
        z_in = zipfile.ZipFile(test_path, 'r')
        z_out = zipfile.ZipFile(self.temp_path, 'r')

        self.assertEqual(
            z_in.namelist(),
            ['agency.txt',
             'calendar_dates.txt',
             'fare_attributes.txt',
             'fare_rules.txt',
             'feed_info.txt',
             'realtime_feeds.txt',
             'route_directions.txt',
             'routes.txt',
             'shapes.txt',
             'stop_features.txt',
             'stop_times.txt',
             'stops.txt',
             'transfers.txt',
             'trips.txt'])
        self.assertEqual(
            z_out.namelist(),
            ['agency.txt',
             'calendar_dates.txt',
             'fare_attributes.txt',
             'fare_rules.txt',
             'feed_info.txt',
             'routes.txt',
             'shapes.txt',
             'stop_times.txt',
             'stops.txt',
             'transfers.txt',
             'trips.txt'])

        agency_in = self.normalize(z_in.read('agency.txt'))
        agency_out = self.normalize(z_out.read('agency.txt'))
        self.assertEqual(agency_in, agency_out)

        cdates_in = self.normalize(z_in.read('calendar_dates.txt'))
        cdates_out = self.normalize(z_out.read('calendar_dates.txt'))
        self.assertEqual(cdates_in, cdates_out)

        fare_in = self.normalize(z_in.read('fare_attributes.txt'))
        self.assertEqual(fare_in, b'''\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
B,2.5,USD,0,,7200
''')
        # Sometimes 2.5000, sometimes 2.5
        fare_b = Fare.objects.get(fare_id='B')
        s_fare_b = text_type(fare_b.price).encode('utf-8')
        fare_out = z_out.read('fare_attributes.txt')
        self.assertEqual(fare_out, b'''\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
B,''' + s_fare_b + b''',USD,0,,7200
''')

        fare_rules_in = self.normalize(z_in.read('fare_rules.txt'))
        fare_rules_out = self.normalize(z_out.read('fare_rules.txt'))
        self.assertEqual(fare_rules_in, b'''\
fare_id,origin_id,route_id,contains_id
B,B,,B
''')
        self.assertEqual(fare_rules_out, b'''\
fare_id,origin_id,contains_id
B,B,B
''')

        routes_in = self.normalize(z_in.read('routes.txt'))
        routes_out = self.normalize(z_out.read('routes.txt'))
        self.assertEqual(routes_in, routes_out)

        shapes_in = self.normalize(z_in.read('shapes.txt'))
        shapes_out = self.normalize(z_out.read('shapes.txt'))
        self.assertEqual(shapes_in, shapes_out)

        stop_times_in = self.normalize(z_in.read('stop_times.txt'))
        stop_times_out = self.normalize(z_out.read('stop_times.txt'))
        self.assertEqual(stop_times_in, stop_times_out)

        stops_in = self.normalize(z_in.read('stops.txt'))
        stops_in_header = stops_in.split(b'\n')[0]
        stops_out = self.normalize(z_out.read('stops.txt'))
        stops_out_header = stops_out.split(b'\n')[0]
        # parent_station in input, not in output
        self.assertEqual(stops_in_header, b'''\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,parent_station,direction,position''')
        self.assertEqual(stops_out_header, b'''\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,direction,position''')

        transfers_in = self.normalize(z_in.read('transfers.txt'))
        transfers_out = self.normalize(z_out.read('transfers.txt'))
        self.assertEqual(transfers_in, transfers_out)

        trips_in = self.normalize(z_in.read('trips.txt'))
        trips_out = self.normalize(z_out.read('trips.txt'))
        # Drops unused trip_type
        self.assertEqual(trips_in, b'''\
route_id,service_id,trip_id,direction_id,block_id,shape_id,trip_type
34,W.411,5215038,0,3401,235511,
''')
        self.assertEqual(trips_out, b'''\
route_id,service_id,trip_id,direction_id,block_id,shape_id
34,W.411,5215038,0,3401,235511
''')
