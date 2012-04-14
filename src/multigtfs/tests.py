import os.path
import StringIO
import urllib

from django.test import TestCase

from multigtfs.models import Feed, Stop, Zone
from multigtfs.utils import (
    import_agency, import_gtfs, import_stops)

my_dir = os.path.dirname(__file__)
test_path = os.path.abspath(os.path.join(my_dir, 'GTFS_Test_Data.zip'))
test_url = (
    "http://timetablepublisher.googlecode.com/files/GTFS%20Test%20Data.zip")

class ImportGTFSTest(TestCase):
    def setUp(self):
        if not os.path.exists(test_path):
            print "Downloading %s to %s..." % (test_url, test_path)
            urllib.urlretrieve(test_url, test_path)
            print "Done."

    def test_import_gtfs(self):
        feed = Feed.objects.create()
        with open(test_path, 'rb') as zip_file:
            import_gtfs(zip_file, feed)


class ImportAgencyTest(TestCase):
    
    def test_import_agency_minimal(self):
        agency_txt = StringIO.StringIO("""\
agency_id,agency_name,agency_url,agency_timezone
DTA,Demo Transit Authority,http://google.com,America/Los_Angeles
""")
        feed = Feed.objects.create()
        agencies = import_agency(agency_txt, feed)
        self.assertEqual(len(agencies), 1)
        agency = agencies[0]
        self.assertEqual(agency.feed, feed)
        self.assertEqual(agency.agency_id, 'DTA')
        self.assertEqual(agency.name, 'Demo Transit Authority')
        self.assertEqual(agency.url, 'http://google.com')
        self.assertEqual(agency.timezone, 'America/Los_Angeles')
        self.assertEqual(agency.lang, '')
        self.assertEqual(agency.phone, '')
        self.assertEqual(agency.fare_url, '')

    def test_import_agency_maximal(self):
        agency_txt = StringIO.StringIO("""\
agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,\
agency_fare_url
DTA,"Demo Transit Authority",http://google.com,America/Los_Angeles,en,\
555-555-TEST,http://google.com
""")
        feed = Feed.objects.create()
        agencies = import_agency(agency_txt, feed)
        self.assertEqual(len(agencies), 1)
        agency = agencies[0]
        self.assertEqual(agency.feed, feed)
        self.assertEqual(agency.agency_id, 'DTA')
        self.assertEqual(agency.name, 'Demo Transit Authority')
        self.assertEqual(agency.url, 'http://google.com')
        self.assertEqual(agency.timezone, 'America/Los_Angeles')
        self.assertEqual(agency.lang, 'en')
        self.assertEqual(agency.phone, '555-555-TEST')
        self.assertEqual(agency.fare_url, 'http://google.com')


class ImportStopsTest(TestCase):
    
    def test_import_stops_minimal(self):
        stops_txt = StringIO.StringIO("""\
stop_id,stop_name,stop_desc,stop_lat,stop_lon
FUR_CREEK_RES,Furnace Creek Resort (Demo),,36.425288,-117.133162
""")
        feed = Feed.objects.create()
        stops = import_stops(stops_txt, feed)
        self.assertEqual(len(stops), 1)
        stop = stops[0]
        self.assertEqual(stop.feed, feed)
        self.assertEqual(stop.stop_id, 'FUR_CREEK_RES')
        self.assertEqual(stop.code, '')
        self.assertEqual(stop.name, 'Furnace Creek Resort (Demo)')
        self.assertEqual(stop.desc, '')
        self.assertEqual(stop.lat, '36.425288')
        self.assertEqual(stop.lon, '-117.133162')
        self.assertEqual(stop.zone, None)
        self.assertEqual(stop.url, '')
        self.assertEqual(stop.location_type, '')
        self.assertEqual(stop.parent_station, None)
        self.assertEqual(stop.timezone, '')

    def test_import_stops_maximal(self):
        stops_txt = StringIO.StringIO("""\
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,\
location_type,parent_station,stop_timezone
FUR_CREEK_STA,,Furnace Creek Station,"Our Station",36.425288,-117.133162,A,\
http://example.com,1,,America/Los_Angeles
FUR_CREEK_RES,FC,Furnace Creek Resort,,36.425288,-117.133162,A,\
http://example.com/fcr,0,FUR_CREEK_STA,
""")
        feed = Feed.objects.create()
        stops = import_stops(stops_txt, feed)
        self.assertEqual(len(stops), 2)
        station = stops[0]
        zone = Zone.objects.get(feed=feed, zone_id='A')
        self.assertEqual(station.feed, feed)
        self.assertEqual(station.stop_id, 'FUR_CREEK_STA')
        self.assertEqual(station.code, '')
        self.assertEqual(station.name, 'Furnace Creek Station')
        self.assertEqual(station.desc, 'Our Station')
        self.assertEqual(station.lat, '36.425288')
        self.assertEqual(station.lon, '-117.133162')
        self.assertEqual(station.zone, zone)
        self.assertEqual(station.url, 'http://example.com')
        self.assertEqual(station.location_type, '1')
        self.assertEqual(station.parent_station, None)
        self.assertEqual(station.timezone, 'America/Los_Angeles')
        stop = stops[1]
        self.assertEqual(stop.feed, feed)
        self.assertEqual(stop.stop_id, 'FUR_CREEK_RES')
        self.assertEqual(stop.code, 'FC')
        self.assertEqual(stop.name, 'Furnace Creek Resort')
        self.assertEqual(stop.desc, '')
        self.assertEqual(stop.lat, '36.425288')
        self.assertEqual(stop.lon, '-117.133162')
        self.assertEqual(stop.zone, zone)
        self.assertEqual(stop.url, 'http://example.com/fcr')
        self.assertEqual(stop.location_type, '0')
        self.assertEqual(stop.parent_station, station)
        self.assertEqual(stop.timezone, '')