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

from django.contrib.gis.geos import MultiLineString
from django.test import TestCase
from django.utils.six import StringIO

from multigtfs.compat import bom_prefix_csv, force_utf8
from multigtfs.models import Feed, Route, Stop, StopTime, Trip, Zone


class StopTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        stop = Stop.objects.create(
            feed=self.feed, stop_id='STEST',
            point="POINT(-117.133162 36.425288)")
        self.assertEqual(str(stop), '%d-STEST' % self.feed.id)

    def test_legacy_lat_long(self):
        stop1 = Stop(feed=self.feed, stop_id='STOP1')
        stop1.lat = 36.425288
        stop1.lon = -117.133162
        stop1.save()
        stop2 = Stop(feed=self.feed, stop_id='STOP2')
        stop2.lon = -117.14
        stop2.lat = 36.43
        stop2.save()
        self.assertEqual(stop1.point.coords, (-117.133162, 36.425288))
        self.assertEqual(stop1.lat, 36.425288)
        self.assertEqual(stop1.lon, -117.133162)
        self.assertEqual(stop2.point.coords, (-117.14, 36.43))
        self.assertEqual(stop2.lat, 36.43)
        self.assertEqual(stop2.lon, -117.14)

    def test_legacy_create_with_lat_lon(self):
        stop = Stop.objects.create(
            feed=self.feed, stop_id='STEST',
            lat="36.425288", lon="-117.133162")
        self.assertEqual(stop.point.coords, (-117.133162, 36.425288))

    def test_import_stops_txt_none(self):
        stops_txt = StringIO("""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon
""")
        Stop.import_txt(stops_txt, self.feed)
        self.assertFalse(Stop.objects.exists())

    def test_import_stops_txt_minimal(self):
        stops_txt = StringIO("""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon
FUR_CREEK_RES,Furnace Creek Resort (Demo),,36.425288,-117.133162
""")
        Stop.import_txt(stops_txt, self.feed)
        stop = Stop.objects.get()
        self.assertEqual(stop.feed, self.feed)
        self.assertEqual(stop.stop_id, 'FUR_CREEK_RES')
        self.assertEqual(stop.code, '')
        self.assertEqual(stop.name, 'Furnace Creek Resort (Demo)')
        self.assertEqual(stop.desc, '')
        self.assertEqual(str(stop.lat), '36.425288')
        self.assertEqual(str(stop.lon), '-117.133162')
        self.assertEqual(stop.zone, None)
        self.assertEqual(stop.url, '')
        self.assertEqual(stop.location_type, '')
        self.assertEqual(stop.parent_station, None)
        self.assertEqual(stop.timezone, '')
        self.assertEqual(stop.wheelchair_boarding, '')

    def test_import_stops_txt_plus_point(self):
        """Test issue #70, latitude / longitude with leading plus sign."""
        stops_txt = StringIO("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,location_type,parent_station
10258,TANEU,TANNEURS,,+49.119799,+06.182966,1,
""")
        Stop.import_txt(stops_txt, self.feed)
        stop = Stop.objects.get()
        self.assertEqual(stop.feed, self.feed)
        self.assertEqual(stop.stop_id, '10258')
        self.assertEqual(stop.code, 'TANEU')
        self.assertEqual(stop.name, 'TANNEURS')
        self.assertEqual(stop.desc, '')
        self.assertEqual(str(stop.lat), '49.119799')
        self.assertEqual(str(stop.lon), '6.182966')
        self.assertEqual(stop.location_type, '1')
        self.assertEqual(stop.parent_station, None)

    def test_import_stops_txt_extra_columns(self):
        stops_txt = StringIO("""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon,platform_code
FUR_CREEK_RES,Furnace Creek Resort (Demo),,36.425288,-117.133162,7
""")
        Stop.import_txt(stops_txt, self.feed)
        stop = Stop.objects.get()
        self.assertEqual(stop.feed, self.feed)
        self.assertEqual(stop.stop_id, 'FUR_CREEK_RES')
        self.assertEqual(stop.code, '')
        self.assertEqual(stop.name, 'Furnace Creek Resort (Demo)')
        self.assertEqual(stop.desc, '')
        self.assertEqual(str(stop.lat), '36.425288')
        self.assertEqual(str(stop.lon), '-117.133162')
        self.assertEqual(stop.zone, None)
        self.assertEqual(stop.url, '')
        self.assertEqual(stop.location_type, '')
        self.assertEqual(stop.parent_station, None)
        self.assertEqual(stop.timezone, '')
        self.assertEqual(stop.wheelchair_boarding, '')
        self.assertEqual({'platform_code': '7'}, stop.extra_data)
        expected = {'extra_columns': {'Stop': ['platform_code']}}
        self.assertEqual(expected, self.feed.meta)

    def test_import_stops_txt_duplicate(self):
        stops_txt = StringIO("""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon
FUR_CREEK_RES,Furnace Creek Resort (Demo),,36.425288,-117.133162
FUR_CREEK_RES,Furnace Creek Resort,,36.42,-117.13
""")
        Stop.import_txt(stops_txt, self.feed)
        stop = Stop.objects.get()
        self.assertEqual(stop.feed, self.feed)
        self.assertEqual(stop.stop_id, 'FUR_CREEK_RES')
        self.assertEqual(stop.name, 'Furnace Creek Resort (Demo)')

    def test_import_stops_txt_maximal(self):
        stops_txt = StringIO("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,parent_station,stop_timezone,wheelchair_boarding
FUR_CREEK_STA,,Furnace Creek Station,"Our Station",36.425288,-117.133162,A,\
http://example.com,1,,America/Los_Angeles,1
FUR_CREEK_RES,FC,Furnace Creek Resort,,36.425288,-117.133162,A,\
http://example.com/fcr,0,FUR_CREEK_STA,
FEZ_CREEK_STA,,Fez Creek Station,"Our Station",36.425288,-117.133162,A,\
http://example.com,1,,America/Los_Angeles
FEZ_CREEK_RES,FC,Fez Creek Resort,,36.425288,-117.133162,A,\
http://example.com/fcr,0,FEZ_CREEK_STA,
""")
        Stop.import_txt(stops_txt, self.feed)
        self.assertEqual(Stop.objects.count(), 4)

        station = Stop.objects.get(stop_id='FUR_CREEK_STA')
        zone = Zone.objects.get(feed=self.feed, zone_id='A')
        self.assertEqual(station.code, '')
        self.assertEqual(station.name, 'Furnace Creek Station')
        self.assertEqual(station.desc, 'Our Station')
        self.assertEqual(str(station.lat), '36.425288')
        self.assertEqual(str(station.lon), '-117.133162')
        self.assertEqual(station.zone, zone)
        self.assertEqual(station.url, 'http://example.com')
        self.assertEqual(station.location_type, '1')
        self.assertEqual(station.parent_station, None)
        self.assertEqual(station.timezone, 'America/Los_Angeles')
        self.assertEqual(station.wheelchair_boarding, '1')

        stop = Stop.objects.get(stop_id='FUR_CREEK_RES')
        self.assertEqual(stop.code, 'FC')
        self.assertEqual(stop.name, 'Furnace Creek Resort')
        self.assertEqual(stop.desc, '')
        self.assertEqual(str(stop.lat), '36.425288')
        self.assertEqual(str(stop.lon), '-117.133162')
        self.assertEqual(stop.zone, zone)
        self.assertEqual(stop.url, 'http://example.com/fcr')
        self.assertEqual(stop.location_type, '0')
        self.assertEqual(stop.parent_station, station)
        self.assertEqual(stop.timezone, '')

        stop2 = Stop.objects.get(stop_id='FEZ_CREEK_RES')
        self.assertEqual(stop2.parent_station.stop_id, 'FEZ_CREEK_STA')

    def test_import_stops_txt_stop_before_station(self):
        '''parent_station is set when the stop comes first'''
        stops_txt = StringIO("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,parent_station,stop_timezone
FUR_CREEK_RES,FC,Furnace Creek Resort,,36.425288,-117.133162,A,\
http://example.com/fcr,0,FUR_CREEK_STA,
FUR_CREEK_STA,,Furnace Creek Station,"Our Station",36.425288,-117.133162,A,\
http://example.com,1,,America/Los_Angeles
""")
        Stop.import_txt(stops_txt, self.feed)
        self.assertEqual(Stop.objects.count(), 2)
        station = Stop.objects.get(stop_id='FUR_CREEK_STA')
        stop = Stop.objects.get(stop_id='FUR_CREEK_RES')
        self.assertEqual(stop.parent_station, station)

    def test_import_stops_txt_stop_before_station_plus_extra(self):
        stops_txt = StringIO("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,parent_station,stop_timezone,extra
FUR_CREEK_RES,FC,Furnace Creek Resort,,36.425288,-117.133162,A,\
http://example.com/fcr,0,FUR_CREEK_STA,,a stop
FUR_CREEK_STA,,Furnace Creek Station,"Our Station",36.425288,-117.133162,A,\
http://example.com,1,,America/Los_Angeles,a station
""")
        Stop.import_txt(stops_txt, self.feed)
        self.assertEqual(Stop.objects.count(), 2)
        station = Stop.objects.get(stop_id='FUR_CREEK_STA')
        stop = Stop.objects.get(stop_id='FUR_CREEK_RES')
        self.assertEqual(stop.parent_station, station)
        self.assertEqual(stop.extra_data, {'extra': 'a stop'})
        self.assertEqual(station.extra_data, {'extra': 'a station'})
        expected = {'extra_columns': {'Stop': ['extra']}}
        self.assertEqual(expected, self.feed.meta)

    def test_import_stops_txt_bom(self):
        stops_txt = StringIO(bom_prefix_csv("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,parent_station,stop_timezone
FUR_CREEK_RES,FC,Furnace Creek Resort,,36.425288,-117.133162,A,\
http://example.com/fcr,0,FUR_CREEK_STA,
FUR_CREEK_STA,,Furnace Creek Station,"Our Station",36.425288,-117.133162,A,\
http://example.com,1,,America/Los_Angeles
"""))
        Stop.import_txt(stops_txt, self.feed)
        self.assertEqual(Stop.objects.count(), 2)
        station = Stop.objects.get(stop_id='FUR_CREEK_STA')
        stop = Stop.objects.get(stop_id='FUR_CREEK_RES')
        self.assertEqual(stop.parent_station, station)

    def test_import_stops_txt_parent_is_space(self):
        """If parent station is an empty string, then leave unset

        Issue #36
        """
        stops_txt = StringIO("""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon,parent_station
FUR_CREEK_RES,Furnace Creek Resort (Demo),,36.425288,-117.133162," "
""")
        Stop.import_txt(stops_txt, self.feed)
        stop = Stop.objects.get()
        self.assertEqual(stop.parent_station, None)

    def test_import_stops_txt_strip_spaces(self):
        """A whitespace-only field is treated as empty.

        From SFMTA feed.
        """
        stops_txt = StringIO("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url
98,198,2ND ST & MARKET ST, ,37.789255,-122.401225, ,%s
""" % ' ')  # Get around flake8 warning on trailing whitespace
        Stop.import_txt(stops_txt, self.feed)
        stop = Stop.objects.get()
        self.assertEqual(stop.name, '2ND ST & MARKET ST')
        self.assertEqual(stop.desc, '')
        self.assertEqual(stop.zone, None)
        self.assertEqual(stop.url, '')

    def test_export_stops_txt_none(self):
        stops_txt = Stop.export_txt(self.feed)
        self.assertFalse(stops_txt)

    def test_export_stops_txt_minimal(self):
        Stop.objects.create(
            feed=self.feed, stop_id='FUR_CREEK_RES',
            name='Furnace Creek Resort (Demo)',
            point="POINT(-117.133162 36.425288)")
        stops_txt = Stop.export_txt(self.feed)
        self.assertEqual(stops_txt, """\
stop_id,stop_name,stop_lat,stop_lon
FUR_CREEK_RES,Furnace Creek Resort (Demo),36.425288,-117.133162
""")

    def test_export_stops_utf8(self):
        Stop.objects.create(
            feed=self.feed, stop_id=6071,
            name=b'The Delta Caf\x82'.decode('latin1'),
            point='POINT(-95.975834 36.114554)')
        stops_txt = force_utf8(Stop.export_txt(self.feed))
        self.assertEqual(stops_txt, b"""\
stop_id,stop_name,stop_lat,stop_lon
6071,The Delta Caf\xc2\x82,36.114554,-95.975834
""")

    def test_export_stops_extra_data(self):
        self.feed.meta = {'extra_columns': {'Stop': ['extra']}}
        self.feed.save()
        Stop.objects.create(
            feed=self.feed, stop_id='FUR_CREEK_RES',
            name='Furnace Creek Resort (Demo)',
            point="POINT(-117.133162 36.425288)",
            extra_data={'extra': '7'})
        stops_txt = Stop.export_txt(self.feed)
        self.assertEqual(stops_txt, """\
stop_id,stop_name,stop_lat,stop_lon,extra
FUR_CREEK_RES,Furnace Creek Resort (Demo),36.425288,-117.133162,7
""")

    def test_update_geometry_on_stop_save(self):
        route = Route.objects.create(feed=self.feed, rtype=3)
        trip = Trip.objects.create(route=route)
        s1 = Stop.objects.create(
            feed=self.feed, point="POINT(-117.133162 36.425288)")
        s2 = Stop.objects.create(
            feed=self.feed, point="POINT(-117.13 36.42)")
        StopTime.objects.create(stop=s1, trip=trip, stop_sequence=1)
        StopTime.objects.create(stop=s2, trip=trip, stop_sequence=2)

        # Starts unset
        trip = Trip.objects.get(id=trip.id)
        route = Route.objects.get(id=route.id)
        self.assertFalse(trip.geometry)

        # Stop save
        s1.save()

        # Now set
        trip = Trip.objects.get(id=trip.id)
        route = Route.objects.get(id=route.id)
        self.assertEqual(
            trip.geometry.coords,
            ((-117.133162, 36.425288), (-117.13, 36.42)))
        self.assertEqual(route.geometry,
                         MultiLineString(trip.geometry, srid=4326))
