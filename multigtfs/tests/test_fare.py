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

from django.test import TestCase
from django.utils.six import StringIO

from multigtfs.models import Feed, Fare


class FareTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        fa = Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD',
            payment_method=0, transfers=0)
        self.assertEqual(str(fa), '%d-p(1.25 USD)' % self.feed.id)

    def test_import_fare_attributes_minimal(self):
        fare_attributes_txt = StringIO("""\
fare_id,price,currency_type,payment_method,transfers
p,1.25,USD,0,0
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()
        self.assertEqual(fa.feed, self.feed)
        self.assertEqual(fa.fare_id, 'p')
        # 1.25 on sqlite, 1.2500 on postgis
        self.assertEqual(str(fa.price)[:4], '1.25')
        self.assertEqual(fa.currency_type, 'USD')
        self.assertEqual(fa.payment_method, 0)
        self.assertEqual(fa.transfers, 0)
        self.assertEqual(fa.transfer_duration, None)

    def test_import_fare_duplicate_fare_id(self):
        fare_attributes_txt = StringIO("""\
fare_id,price,currency_type,payment_method,transfers
p,1.25,USD,0,0
p,1.25,USD,0,0
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()  # Just one
        self.assertEqual(fa.feed, self.feed)
        self.assertEqual(fa.fare_id, 'p')

    def test_import_fare_attributes_maximal(self):
        fare_attributes_txt = StringIO("""\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,1.25,USD,0,0,60
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()
        self.assertEqual(fa.transfer_duration, 60)

    def test_import_fare_attributes_omitted(self):
        fare_attributes_txt = StringIO("""\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,1.25,USD,0,0
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()
        self.assertEqual(fa.fare_id, 'p')
        self.assertEqual(fa.transfer_duration, None)

    def test_import_fare_attributes_unlimited_transfers(self):
        fare_attributes_txt = StringIO("""\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,1.25,USD,0,,3600
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()
        self.assertEqual(fa.fare_id, 'p')
        self.assertEqual(fa.transfers, None)
        self.assertEqual(fa.transfer_duration, 3600)

    def test_export_fare_attributes_minimal(self):
        Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD',
            payment_method=0, transfers=0)
        fare = Fare.objects.get()
        fare_txt = Fare.export_txt(self.feed)
        self.assertEqual(fare_txt, """\
fare_id,price,currency_type,payment_method,transfers
p,%s,USD,0,0
""" % fare.price)

    def test_export_fare_attributes_maximal(self):
        Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD',
            payment_method=0, transfers=0, transfer_duration=3600)
        fare = Fare.objects.get()
        fare_txt = Fare.export_txt(self.feed)
        self.assertEqual(fare_txt, """\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,%s,USD,0,0,3600
""" % fare.price)

    def test_export_fare_attributes_unlimited_transfers(self):
        Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD',
            payment_method=0, transfers=None, transfer_duration=3600)
        fare = Fare.objects.get()
        fare_txt = Fare.export_txt(self.feed)
        self.assertEqual(fare_txt, """\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,%s,USD,0,,3600
""" % fare.price)
