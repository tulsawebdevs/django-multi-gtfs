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

from django.test import TestCase
from django.utils.six import StringIO

from multigtfs.models import Agency, Feed
from multigtfs.compat import bom_prefix_csv


class AgencyTest(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        agency = Agency.objects.create(feed=self.feed, agency_id='TEST')
        self.assertEqual(str(agency), '%d-TEST' % self.feed.id)

    def test_import_minimal(self):
        agency_txt = StringIO("""\
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

    def test_import_two_no_id(self):
        agency_txt = StringIO("""\
agency_name,agency_url,agency_timezone
Demo Transit Authority,http://google.com,America/Los_Angeles
Example Transit Authority,http://example.com,America/Los_Angeles
""")
        Agency.import_txt(agency_txt, self.feed)
        agency = Agency.objects.get()  # Just one
        self.assertEqual(agency.agency_id, '')
        self.assertEqual(agency.name, 'Demo Transit Authority')

    def test_import_two_same_id(self):
        agency_txt = StringIO("""\
agency_id,agency_name,agency_url,agency_timezone
DTA,Demo Transit Authority,http://google.com,America/Los_Angeles
DTA,Example Transit Authority,http://example.com,America/Los_Angeles
""")
        Agency.import_txt(agency_txt, self.feed)
        agency = Agency.objects.get()  # Just one
        self.assertEqual(agency.agency_id, 'DTA')
        self.assertEqual(agency.name, 'Demo Transit Authority')

    def test_import_agency_maximal(self):
        agency_txt = StringIO("""\
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

    def test_import_bom(self):
        agency_txt = StringIO(bom_prefix_csv("""\
agency_name,agency_url,agency_timezone
Demo Transit Authority,http://google.com,America/Los_Angeles
"""))
        Agency.import_txt(agency_txt, self.feed)
        agency = Agency.objects.get()
        self.assertEqual(agency.agency_id, '')
        self.assertEqual(agency.name, 'Demo Transit Authority')
        self.assertEqual(agency.url, 'http://google.com')
        self.assertEqual(agency.timezone, 'America/Los_Angeles')
        self.assertEqual(agency.lang, '')
        self.assertEqual(agency.phone, '')
        self.assertEqual(agency.fare_url, '')

    def test_export_agency_none(self):
        agency_txt = Agency.export_txt(self.feed)
        self.assertFalse(agency_txt)

    def test_export_agency_minimal(self):
        Agency.objects.create(
            feed=self.feed, name='Demo Transit Authority',
            url='http://google.com', timezone='America/Los_Angeles')
        agency_txt = Agency.export_txt(self.feed)
        self.assertEqual(agency_txt, """\
agency_name,agency_url,agency_timezone
Demo Transit Authority,http://google.com,America/Los_Angeles
""")

    def test_export_agency_maximal(self):
        Agency.objects.create(
            feed=self.feed, agency_id='DTA', name='Demo Transit Authority',
            url='http://google.com', timezone='America/Los_Angeles',
            lang='en', phone='555-555-TEST', fare_url='http://google.com')
        agency_txt = Agency.export_txt(self.feed)
        self.assertEqual(agency_txt, """\
agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,\
agency_fare_url
DTA,Demo Transit Authority,http://google.com,America/Los_Angeles,en,\
555-555-TEST,http://google.com
""")
