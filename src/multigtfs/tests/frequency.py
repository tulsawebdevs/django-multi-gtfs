{'headway_secs': '1800', 'start_time': '6:00:00', 'trip_id': 'STBA', 'end_time': '22:00:00'}

from datetime import date, time
import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Frequency, Route, Service, Trip
from multigtfs.utils import import_frequencies


class FrequencyTests(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.route = Route.objects.create(
            feed=self.feed, route_id='R1', rtype=3)
        self.service = Service.objects.create(
            feed=self.feed, service_id='S1', start_date=date(2011,4,14),
            end_date=date(2011,12,31))
        self.trip = Trip.objects.create(route=self.route, trip_id='STBA')
        self.trip.services.add(self.service)

    def test_string(self):
        frequency = Frequency.objects.create(
            trip=self.trip, start_time='6:00', end_time='22:00',
            headway_secs=1800)
        self.assertEqual(str(frequency), '1-R1-STBA')

    def test_import_frequencies_minimal(self):
        frequencies_txt = StringIO.StringIO("""\
trip_id,start_time,end_time,headway_secs
STBA,6:00:00,22:00:00,1800
""")
        import_frequencies(frequencies_txt, self.feed)
        frequency = Frequency.objects.get()
        self.assertEqual(frequency.trip, self.trip)
        self.assertEqual(frequency.start_time, time(6))
        self.assertEqual(frequency.end_time, time(22))
        self.assertEqual(frequency.headway_secs, 1800)
        self.assertEqual(frequency.exact_times, '')

    def test_import_frequencies_maximal(self):
        frequencies_txt = StringIO.StringIO("""\
trip_id,start_time,end_time,headway_secs,exact_times
STBA,6:00:00,22:00:00,1800,1
""")
        import_frequencies(frequencies_txt, self.feed)
        frequency = Frequency.objects.get()
        self.assertEqual(frequency.trip, self.trip)
        self.assertEqual(frequency.start_time, time(6))
        self.assertEqual(frequency.end_time, time(22))
        self.assertEqual(frequency.headway_secs, 1800)
        self.assertEqual(frequency.exact_times, '1')
