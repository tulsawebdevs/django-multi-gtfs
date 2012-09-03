import StringIO

from django.test import TestCase

from multigtfs.models import Agency, Feed


class AgencyTest(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        self.assertEqual(self.feed.id, 1)
        agency = Agency.objects.create(feed=self.feed, agency_id='TEST')
        self.assertEqual(str(agency), '1-TEST')

    def test_import_minimal(self):
        agency_txt = StringIO.StringIO("""\
agency_name,agency_url,agency_timezone
Demo Transit Authority,http://google.com,America/Los_Angeles
""")
        Agency.import_txt(agency_txt, self.feed)
        agency = Agency.objects.get()
        self.assertEqual(agency.agency_id, '')
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
        Agency.import_txt(agency_txt, self.feed)
        agency = Agency.objects.get()
        self.assertEqual(agency.agency_id, 'DTA')
        self.assertEqual(agency.name, 'Demo Transit Authority')
        self.assertEqual(agency.url, 'http://google.com')
        self.assertEqual(agency.timezone, 'America/Los_Angeles')
        self.assertEqual(agency.lang, 'en')
        self.assertEqual(agency.phone, '555-555-TEST')
        self.assertEqual(agency.fare_url, 'http://google.com')

    def test_export_agency_none(self):
        agency_txt = Agency.objects.in_feed(self.feed).export_txt()
        self.assertFalse(agency_txt)

    def test_export_agency_minimal(self):
        Agency.objects.create(
            feed=self.feed, name='Demo Transit Authority',
            url='http://google.com', timezone='America/Los_Angeles')
        agency_txt = Agency.objects.in_feed(self.feed).export_txt()
        self.assertEqual(agency_txt, """\
agency_name,agency_url,agency_timezone
Demo Transit Authority,http://google.com,America/Los_Angeles
""")

    def test_export_agency_maximal(self):
        Agency.objects.create(
            feed=self.feed, agency_id='DTA', name='Demo Transit Authority',
            url='http://google.com', timezone='America/Los_Angeles',
            lang='en', phone='555-555-TEST', fare_url='http://google.com')
        agency_txt = Agency.objects.in_feed(self.feed).export_txt()
        self.assertEqual(agency_txt, """\
agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,\
agency_fare_url
DTA,Demo Transit Authority,http://google.com,America/Los_Angeles,en,\
555-555-TEST,http://google.com
""")
