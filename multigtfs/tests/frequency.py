#
# Copyright 2012 John Whitlock
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

from datetime import date
import StringIO

from django.core.serializers import serialize
from django.test import TestCase

from multigtfs.models import Feed, Frequency, Route, Service, Trip
from multigtfs.models.fields import Seconds


class FrequencyTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.route = Route.objects.create(
            feed=self.feed, route_id='R1', rtype=3)
        self.service = Service.objects.create(
            feed=self.feed, service_id='S1', start_date=date(2011, 4, 14),
            end_date=date(2011, 12, 31))
        self.trip = Trip.objects.create(route=self.route, trip_id='STBA')
        self.trip.services.add(self.service)

    def test_string(self):
        frequency = Frequency.objects.create(
            trip=self.trip, start_time='6:00', end_time='22:00',
            headway_secs=1800)
        self.assertEqual(str(frequency), '1-R1-STBA')

    def test_import_frequencies_txt_minimal(self):
        frequencies_txt = StringIO.StringIO("""\
trip_id,start_time,end_time,headway_secs
STBA,6:00:00,22:00:00,1800
""")
        Frequency.import_txt(frequencies_txt, self.feed)
        frequency = Frequency.objects.get()
        self.assertEqual(frequency.trip, self.trip)
        self.assertEqual(frequency.start_time, Seconds.from_hms(hours=6))
        self.assertEqual(frequency.end_time, Seconds.from_hms(hours=22))
        self.assertEqual(frequency.headway_secs, 1800)
        self.assertEqual(frequency.exact_times, '')

    def test_import_frequencies_txt_maximal(self):
        frequencies_txt = StringIO.StringIO("""\
trip_id,start_time,end_time,headway_secs,exact_times
STBA,6:00:00,23:30:35,1800,1
""")
        Frequency.import_txt(frequencies_txt, self.feed)
        frequency = Frequency.objects.get()
        self.assertEqual(frequency.trip, self.trip)
        self.assertEqual(frequency.start_time, Seconds.from_hms(hours=6))
        self.assertEqual(frequency.end_time, Seconds.from_hms(23, 30, 35))
        self.assertEqual(frequency.headway_secs, 1800)
        self.assertEqual(frequency.exact_times, '1')

    def test_import_frequencies_txt_omitted_with_rollover(self):
        frequencies_txt = StringIO.StringIO("""\
trip_id,start_time,end_time,headway_secs,exact_times
STBA,00:50:00,24:10:00,1800,
""")
        Frequency.import_txt(frequencies_txt, self.feed)
        frequency = Frequency.objects.get()
        self.assertEqual(str(frequency.start_time), '00:50:00')
        self.assertEqual(frequency.end_time, Seconds.from_hms(24, 10))
        self.assertEqual(frequency.headway_secs, 1800)
        self.assertEqual(frequency.exact_times, '')

    def test_export_frequencies_txt_none(self):
        frequencies_txt = Frequency.objects.in_feed(self.feed).export_txt()
        self.assertEqual(frequencies_txt, None)

    def test_export_frequencies_txt_minimal(self):
        Frequency.objects.create(
            trip=self.trip, start_time=Seconds.from_hms(hours=6),
            end_time=Seconds.from_hms(hours=22), headway_secs=1800)
        frequencies_txt = Frequency.objects.in_feed(self.feed).export_txt()
        self.assertEqual(frequencies_txt, """\
trip_id,start_time,end_time,headway_secs
STBA,06:00:00,22:00:00,1800
""")

    def test_export_frequencies_txt_maximal(self):
        Frequency.objects.create(
            trip=self.trip, start_time='05:00', end_time='25:00',
            headway_secs=1800)
        frequencies_txt = Frequency.objects.in_feed(self.feed).export_txt()
        self.assertEqual(frequencies_txt, """\
trip_id,start_time,end_time,headway_secs
STBA,05:00:00,25:00:00,1800
""")

    def test_serialize(self):
        '''Test serialization of Frequency, which has a SecondsField'''
        Frequency.objects.create(
            trip=self.trip, start_time='05:00', end_time='25:00',
            headway_secs=1800)
        json = serialize('json', Frequency.objects.all())
        self.assertEqual(
            json,
            '[{"pk": 1, "model": "multigtfs.frequency",'
            ' "fields": {"exact_times": "", "start_time": "05:00:00",'
            ' "headway_secs": 1800, "trip": 1, "end_time": "25:00:00"}}]')
