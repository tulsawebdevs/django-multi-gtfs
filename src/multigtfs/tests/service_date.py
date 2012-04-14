from datetime import date
import StringIO

from django.test import TestCase

from multigtfs.models import Calendar, CalendarDate, Feed
from multigtfs.utils import import_calendar_dates

class CalendarDateTest(TestCase):
    def test_string(self):
        feed = Feed.objects.create()
        self.assertEqual(feed.id, 1)
        calendar = Calendar.objects.create(
            feed=feed, service_id='S1', start_date=date(2011,4,14), 
            end_date=date(2011,12,31))
        calendar_date = CalendarDate.objects.create(
            date=date(2012, 4, 14), service=calendar, exception_type=2)
        self.assertEqual(str(calendar_date), '1-S1 2012-04-14 Removed')
        calendar_date.exception_type = 1
        self.assertEqual(str(calendar_date), '1-S1 2012-04-14 Added')


class ImportCalendarDatesTest(TestCase):

    def test_import_calendar_dates(self):
        calendar_dates_txt = StringIO.StringIO("""\
date,service_id,exception_type
20120414,S1,2
""")
        feed = Feed.objects.create()
        service = Calendar.objects.create(
            feed=feed, service_id='S1', start_date=date(2011,4,1), 
            end_date=date(2011,12,31))
        import_calendar_dates(calendar_dates_txt, feed)
        calendar_date = CalendarDate.objects.get()
        self.assertEqual(calendar_date.date, date(2012,4,14))
        self.assertEqual(calendar_date.service, service)
        self.assertEqual(calendar_date.exception_type, 2)
