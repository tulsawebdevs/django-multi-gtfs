import StringIO

from django.test import TestCase

from multigtfs.models import Agency, Feed
from multigtfs.utils import import_agency


class AgencyTests(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        self.assertEqual(self.feed.id, 1)
        agency = Agency.objects.create(feed=self.feed, agency_id='TEST')
        self.assertEqual(str(agency), '1-TEST')

    def test_import_agency_minimal(self):
        agency_txt = StringIO.StringIO("""\
agency_id,agency_name,agency_url,agency_timezone
DTA,Demo Transit Authority,http://google.com,America/Los_Angeles
""")
        import_agency(agency_txt, self.feed)
        agency = Agency.objects.get()
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
        import_agency(agency_txt, self.feed)
        agency = Agency.objects.get()
        self.assertEqual(agency.agency_id, 'DTA')
        self.assertEqual(agency.name, 'Demo Transit Authority')
        self.assertEqual(agency.url, 'http://google.com')
        self.assertEqual(agency.timezone, 'America/Los_Angeles')
        self.assertEqual(agency.lang, 'en')
        self.assertEqual(agency.phone, '555-555-TEST')
        self.assertEqual(agency.fare_url, 'http://google.com')
