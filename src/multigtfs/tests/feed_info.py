from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, FeedInfo
from multigtfs.models.feed_info import import_feed_info_txt


class FeedInfoTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        feed_info = FeedInfo.objects.create(
            feed=self.feed, publisher_name='PTEST',
            publisher_url='http://example.com', lang='en')
        self.assertEqual(str(feed_info), '1-PTEST')

    def test_import_feed_info_txt_maximal(self):
        feed_info_txt = StringIO.StringIO("""\
feed_publisher_name,feed_publisher_url,feed_lang,feed_start_date,\
feed_end_date,feed_version
PTEST,http://example.com,en,20120414,20121231,FOO1
""")
        import_feed_info_txt(feed_info_txt, feed=self.feed)
        feed_info = FeedInfo.objects.get()
        self.assertEqual(feed_info.publisher_name, 'PTEST')
        self.assertEqual(feed_info.publisher_url, 'http://example.com')
        self.assertEqual(feed_info.lang, 'en')
        self.assertEqual(feed_info.start_date, date(2012, 4, 14))
        self.assertEqual(feed_info.end_date, date(2012, 12, 31))
        self.assertEqual(feed_info.version, 'FOO1')

    def test_import_feed_info_txt_minimal(self):
        feed_info_txt = StringIO.StringIO("""\
feed_publisher_name,feed_publisher_url
PTEST,http://example.com
""")
        import_feed_info_txt(feed_info_txt, feed=self.feed)
        feed_info = FeedInfo.objects.get()
        self.assertEqual(feed_info.publisher_name, 'PTEST')
        self.assertEqual(feed_info.publisher_url, 'http://example.com')
        self.assertEqual(feed_info.lang, '')
        self.assertEqual(feed_info.start_date, None)
        self.assertEqual(feed_info.end_date, None)
        self.assertEqual(feed_info.version, '')
