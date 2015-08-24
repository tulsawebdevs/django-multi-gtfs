#
# Copyright 2012-2014 John Whitlock
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

from __future__ import unicode_literals
from datetime import date

from django.test import TestCase
from django.utils.six import StringIO

from multigtfs.models import Feed, Service


class ServiceTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        service = Service.objects.create(
            feed=self.feed, service_id='S1', start_date=date(2011, 4, 14),
            end_date=date(2011, 12, 31))
        self.assertEqual(str(service), '%d-S1' % self.feed.id)

    def test_import_calendar_txt(self):
        calendar_txt = StringIO("""\
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
start_date,end_date
W,1,0,1,0,1,0,1,20120414,20121231
""")
        Service.import_txt(calendar_txt, self.feed)
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

    def test_import_calendar_duplicate(self):
        calendar_txt = StringIO("""\
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
start_date,end_date
W,1,0,1,0,1,0,1,20120414,20121231
W,0,1,0,1,0,1,0,20120414,20121231
""")
        Service.import_txt(calendar_txt, self.feed)
        service = Service.objects.get()  # Only one
        self.assertEqual(service.feed, self.feed)
        self.assertEqual(service.service_id, 'W')

    def test_export_calendar_txt_none(self):
        calendar_txt = Service.export_txt(self.feed)
        self.assertFalse(calendar_txt)

    def test_export_calendar_txt(self):
        Service.objects.create(
            feed=self.feed, service_id='W', monday=True, tuesday=False,
            wednesday=True, thursday=False, friday=True, saturday=False,
            sunday=True, start_date=date(2012, 7, 17),
            end_date=date(2013, 7, 17))
        calendar_txt = Service.export_txt(self.feed)
        self.assertEqual(calendar_txt, """\
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
start_date,end_date
W,1,0,1,0,1,0,1,20120717,20130717
""")
