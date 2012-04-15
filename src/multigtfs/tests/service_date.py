from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Service, ServiceDate
from multigtfs.utils import import_calendar_dates

class ServiceDateTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.service = Service.objects.create(
            feed=self.feed, service_id='S1', start_date=date(2011,4,14),
            end_date=date(2011,12,31))

    def test_string(self):
        service_date = ServiceDate.objects.create(
            date=date(2012, 4, 14), service=self.service, exception_type=2)
        self.assertEqual(str(service_date), '1-S1 2012-04-14 Removed')
        service_date.exception_type = 1
        self.assertEqual(str(service_date), '1-S1 2012-04-14 Added')

    def test_import_service_dates(self):
        calendar_dates_txt = StringIO.StringIO("""\
date,service_id,exception_type
20120414,S1,2
""")
        import_calendar_dates(calendar_dates_txt, self.feed)
        service_date = ServiceDate.objects.get()
        self.assertEqual(service_date.date, date(2012,4,14))
        self.assertEqual(service_date.service, self.service)
        self.assertEqual(service_date.exception_type, 2)
