from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Service
from multigtfs.models.service import (
    import_calendar_txt, export_calendar_txt)


class ServiceTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        service = Service.objects.create(
            feed=self.feed, service_id='S1', start_date=date(2011, 4, 14),
            end_date=date(2011, 12, 31))
        self.assertEqual(str(service), '1-S1')

    def test_import_calendar_txt(self):
        calendar_txt = StringIO.StringIO("""\
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
start_date,end_date
W,1,0,1,0,1,0,1,20120414,20121231
""")
        import_calendar_txt(calendar_txt, self.feed)
        service = Service.objects.get()
        self.assertEqual(service.feed, self.feed)
        self.assertEqual(service.service_id, 'W')
        self.assertTrue(service.monday)
        self.assertFalse(service.tuesday)
        self.assertTrue(service.wednesday)
        self.assertFalse(service.thursday)
        self.assertTrue(service.friday)
        self.assertFalse(service.saturday)
        self.assertTrue(service.sunday)
        self.assertEqual(service.start_date, date(2012, 4, 14))
        self.assertEqual(service.end_date, date(2012, 12, 31))

    def test_export_calendar_txt(self):
        service = Service.objects.create(
            feed=self.feed, service_id='W', monday=True, tuesday=False,
            wednesday=True, thursday=False, friday=True, saturday=False,
            sunday=True, start_date=date(2012, 7, 17),
            end_date=date(2013, 7, 17))
        calendar_txt = export_calendar_txt(self.feed)
        self.assertEqual(calendar_txt, """\
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
start_date,end_date
W,1,0,1,0,1,0,1,20120717,20130717
""")
