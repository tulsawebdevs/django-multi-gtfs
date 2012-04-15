from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Service
from multigtfs.utils import import_calendar


class ServiceTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        service = Service.objects.create(
            feed=self.feed, service_id='S1', start_date=date(2011,4,14),
            end_date=date(2011,12,31))
        self.assertEqual(str(service), '1-S1')

    def test_import_calendar(self):
        calendar_txt = StringIO.StringIO("""\
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
start_date,end_date
W,1,0,1,0,1,0,1,20120414,20121231
""")
        feed = Feed.objects.create()
        import_calendar(calendar_txt, feed)
        service = Service.objects.get()
        self.assertEqual(service.feed, feed)
        self.assertEqual(service.service_id, 'W')
        self.assertTrue(service.monday)
        self.assertFalse(service.tuesday)
        self.assertTrue(service.wednesday)
        self.assertFalse(service.thursday)
        self.assertTrue(service.friday)
        self.assertFalse(service.saturday)
        self.assertTrue(service.sunday)
        self.assertEqual(service.start_date, date(2012,4,14))
        self.assertEqual(service.end_date, date(2012,12,31))
