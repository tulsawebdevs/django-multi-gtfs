from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Service, ServiceDate
from multigtfs.models.service_date import (
    import_calendar_dates_txt, export_calendar_dates_txt)


class ServiceDateTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.service = Service.objects.create(
            feed=self.feed, service_id='S1', start_date=date(2011, 4, 14),
            end_date=date(2012, 12, 31))

    def test_string(self):
        service_date = ServiceDate.objects.create(
            date=date(2012, 4, 14), service=self.service, exception_type=2)
        self.assertEqual(str(service_date), '1-S1 2012-04-14 Removed')
        service_date.exception_type = 1
        self.assertEqual(str(service_date), '1-S1 2012-04-14 Added')

    def test_import_calendar_dates_txt(self):
        calendar_dates_txt = StringIO.StringIO("""\
service_id,date,exception_type
S1,20120414,2
""")
        import_calendar_dates_txt(calendar_dates_txt, self.feed)
        service_date = ServiceDate.objects.get()
        self.assertEqual(service_date.date, date(2012, 4, 14))
        self.assertEqual(service_date.service, self.service)
        self.assertEqual(service_date.exception_type, 2)

    def test_export_calendar_dates_txt_none(self):
        calendar_dates_txt = export_calendar_dates_txt(self.feed)
        self.assertFalse(calendar_dates_txt)

    def test_export_calendar_dates_txt(self):
        service_date1 = ServiceDate.objects.create(
            date=date(2012, 8, 31), service=self.service, exception_type=2)
        service_date2 = ServiceDate.objects.create(
            date=date(2012, 9, 1), service=self.service, exception_type=1)
        calendar_dates_txt = export_calendar_dates_txt(self.feed)
        self.assertEqual(calendar_dates_txt, """\
service_id,date,exception_type
S1,20120831,2
S1,20120901,1
""")
