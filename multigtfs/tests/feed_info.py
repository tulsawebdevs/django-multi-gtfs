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
from datetime import date

from django.test import TestCase
from django.utils.six import StringIO

from multigtfs.models import Feed, FeedInfo


class FeedInfoTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        feed_info = FeedInfo.objects.create(
            feed=self.feed, publisher_name='PTEST',
            publisher_url='http://example.com', lang='en')
        self.assertEqual(str(feed_info), '%d-PTEST' % self.feed.id)

    def test_import_feed_info_txt_maximal(self):
        feed_info_txt = StringIO("""\
feed_publisher_name,feed_publisher_url,feed_lang,feed_start_date,\
feed_end_date,feed_version
PTEST,http://example.com,en,20120414,20121231,FOO1
""")
        FeedInfo.import_txt(feed_info_txt, feed=self.feed)
        feed_info = FeedInfo.objects.get()
        self.assertEqual(feed_info.publisher_name, 'PTEST')
        self.assertEqual(feed_info.publisher_url, 'http://example.com')
        self.assertEqual(feed_info.lang, 'en')
        self.assertEqual(feed_info.start_date, date(2012, 4, 14))
        self.assertEqual(feed_info.end_date, date(2012, 12, 31))
        self.assertEqual(feed_info.version, 'FOO1')

    def test_import_feed_info_txt_minimal(self):
        feed_info_txt = StringIO("""\
feed_publisher_name,feed_publisher_url
PTEST,http://example.com
""")
        FeedInfo.import_txt(feed_info_txt, feed=self.feed)
        feed_info = FeedInfo.objects.get()
        self.assertEqual(feed_info.publisher_name, 'PTEST')
        self.assertEqual(feed_info.publisher_url, 'http://example.com')
        self.assertEqual(feed_info.lang, '')
        self.assertEqual(feed_info.start_date, None)
        self.assertEqual(feed_info.end_date, None)
        self.assertEqual(feed_info.version, '')

    def test_import_feed_info_txt_duplicate(self):
        feed_info_txt = StringIO("""\
feed_publisher_name,feed_publisher_url
PTEST,http://example.com
PTEST,http://www.example.com
""")
        FeedInfo.import_txt(feed_info_txt, feed=self.feed)
        feed_info = FeedInfo.objects.get()  # Just one
        self.assertEqual(feed_info.publisher_name, 'PTEST')
        self.assertEqual(feed_info.publisher_url, 'http://example.com')

    def test_export_feed_info_txt_empty(self):
        feed_info_txt = FeedInfo.export_txt(self.feed)
        self.assertFalse(feed_info_txt)

    def test_export_feed_info_txt_minimal(self):
        FeedInfo.objects.create(
            feed=self.feed, publisher_name='PTEST',
            publisher_url='http://example.com', lang='en')
        feed_info_txt = FeedInfo.export_txt(self.feed)
        self.assertEqual(feed_info_txt, """\
feed_publisher_name,feed_publisher_url,feed_lang
PTEST,http://example.com,en
""")

    def test_export_feed_info_txt_maximal(self):
        FeedInfo.objects.create(
            feed=self.feed, publisher_name='PTEST',
            publisher_url='http://example.com', lang='en',
            start_date=date(2012, 9, 2), end_date=date(2013, 1, 1),
            version='BAR1')
        feed_info_txt = FeedInfo.export_txt(self.feed)
        self.assertEqual(feed_info_txt, """\
feed_publisher_name,feed_publisher_url,feed_lang,feed_start_date,\
feed_end_date,feed_version
PTEST,http://example.com,en,20120902,20130101,BAR1
""")
