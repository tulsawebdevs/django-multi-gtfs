#
# Copyright 2012 John Whitlock
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

import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Stop, Zone


class StopTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        stop = Stop.objects.create(
            feed=self.feed, stop_id='STEST',
            lat="36.425288", lon="-117.133162")
        self.assertEqual(str(stop), '1-STEST')

    def test_import_stops_txt_none(self):
        stops_txt = StringIO.StringIO("""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon
""")
        Stop.import_txt(stops_txt, self.feed)
        self.assertFalse(Stop.objects.exists())

    def test_import_stops_txt_minimal(self):
        stops_txt = StringIO.StringIO("""\
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

    def test_import_stops_txt_maximal(self):
        stops_txt = StringIO.StringIO("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,parent_station,stop_timezone
FUR_CREEK_STA,,Furnace Creek Station,"Our Station",36.425288,-117.133162,A,\
http://example.com,1,,America/Los_Angeles
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
        stops_txt = StringIO.StringIO("""\
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

    def test_export_stops_txt_none(self):
        stops_txt = Stop.objects.in_feed(self.feed).export_txt()
        self.assertFalse(stops_txt)

    def test_export_stops_txt_minimual(self):
        Stop.objects.create(
            feed=self.feed, stop_id='FUR_CREEK_RES',
            name='Furnace Creek Resort (Demo)', lat='36.425288',
            lon='-117.133162')
        stops_txt = Stop.objects.in_feed(self.feed).export_txt()
        self.assertEqual(stops_txt, """\
stop_id,stop_name,stop_lat,stop_lon
FUR_CREEK_RES,Furnace Creek Resort (Demo),36.425288,-117.133162
""")

    def test_export_stops_utf8(self):
        Stop.objects.create(
            feed=self.feed, stop_id=6071,
            name='The Delta Caf\x82'.decode('latin1'), lat='36.114554',
            lon='-95.975834')
        stops_txt = Stop.objects.in_feed(self.feed).export_txt()
        self.assertEqual(stops_txt, """\
stop_id,stop_name,stop_lat,stop_lon
6071,The Delta Caf\xc2\x82,36.114554,-95.975834
""")
