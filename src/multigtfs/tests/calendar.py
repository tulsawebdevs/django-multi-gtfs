import datetime
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Calendar
from multigtfs.utils import import_calendar

class ImportCalendarsTest(TestCase):

    def test_import_calendar(self):
        calendar_txt = StringIO.StringIO("""\
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
start_date,end_date
W,1,0,1,0,1,0,1,20120414,20121231
""")
        feed = Feed.objects.create()
        import_calendar(calendar_txt, feed)
        calendar = Calendar.objects.get()
        self.assertEqual(calendar.feed, feed)
        self.assertEqual(calendar.service_id, 'W')
        self.assertTrue(calendar.monday)
        self.assertFalse(calendar.tuesday)
        self.assertTrue(calendar.wednesday)
        self.assertFalse(calendar.thursday)
        self.assertTrue(calendar.friday)
        self.assertFalse(calendar.saturday)
        self.assertTrue(calendar.sunday)
        self.assertEqual(calendar.start_date, datetime.date(2012,4,14))
        self.assertEqual(calendar.end_date, datetime.date(2012,12,31))
