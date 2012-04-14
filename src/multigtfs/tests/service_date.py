from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Service, ServiceDate
from multigtfs.utils import import_calendar_dates

class ServiceDateTest(TestCase):
    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(feed.id, 1)
        service = Service.objects.create(
            feed=feed, service_id='S1', start_date=date(2011,4,14), 
            end_date=date(2011,12,31))
        service_date = ServiceDate.objects.create(
            date=date(2012, 4, 14), service=service, exception_type=2)
        self.assertEqual(str(service_date), '1-S1 2012-04-14 Removed')
        service_date.exception_type = 1
        self.assertEqual(str(service_date), '1-S1 2012-04-14 Added')


class ImportServiceDatesTest(TestCase):

    def test_import_service_dates(self):
        calendar_dates_txt = StringIO.StringIO("""\
date,service_id,exception_type
20120414,S1,2
""")
        feed = Feed.objects.create()
        service = Service.objects.create(
            feed=feed, service_id='S1', start_date=date(2011,4,1), 
            end_date=date(2011,12,31))
        import_calendar_dates(calendar_dates_txt, feed)
        service_date = ServiceDate.objects.get()
        self.assertEqual(service_date.date, date(2012,4,14))
        self.assertEqual(service_date.service, service)
        self.assertEqual(service_date.exception_type, 2)
