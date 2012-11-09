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

from django.test import TestCase

from multigtfs.models import Feed, Service, ServiceDate


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
        ServiceDate.import_txt(calendar_dates_txt, self.feed)
        service_date = ServiceDate.objects.get()
        self.assertEqual(service_date.date, date(2012, 4, 14))
        self.assertEqual(service_date.service, self.service)
        self.assertEqual(service_date.exception_type, 2)

    def test_export_calendar_dates_txt_none(self):
        cdates_txt = ServiceDate.objects.in_feed(self.feed).export_txt()
        self.assertFalse(cdates_txt)

    def test_export_calendar_dates_txt(self):
        ServiceDate.objects.create(
            date=date(2012, 8, 31), service=self.service, exception_type=2)
        ServiceDate.objects.create(
            date=date(2012, 9, 1), service=self.service, exception_type=1)
        cdates_txt = ServiceDate.objects.in_feed(self.feed).export_txt()
        self.assertEqual(cdates_txt, """\
service_id,date,exception_type
S1,20120831,2
S1,20120901,1
""")
