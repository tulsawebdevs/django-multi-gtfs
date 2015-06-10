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

from multigtfs.models import Feed, Stop, Transfer


class TransferTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.stop1 = Stop.objects.create(
            feed=self.feed, stop_id='STOP1', point="POINT(-117.1 36.4)")
        self.stop2 = Stop.objects.create(
            feed=self.feed, stop_id='STOP2', point="POINT(-117.2 36.5)")

    def test_string(self):
        transfer = Transfer.objects.create(
            from_stop=self.stop1, to_stop=self.stop2)
        self.assertEqual(str(transfer), '%d-STOP1-STOP2' % self.feed.id)

    def test_import_transfers_txt_minimal(self):
        transfers_txt = StringIO("""\
from_stop_id,to_stop_id
STOP1,STOP2
""")
        Transfer.import_txt(transfers_txt, self.feed)
        transfer = Transfer.objects.get()
        self.assertEqual(transfer.from_stop, self.stop1)
        self.assertEqual(transfer.to_stop, self.stop2)
        self.assertEqual(transfer.transfer_type, 0)
        self.assertEqual(transfer.min_transfer_time, None)

    def test_import_transfers_txt_duplicate(self):
        transfers_txt = StringIO("""\
from_stop_id,to_stop_id
STOP1,STOP2
STOP1,STOP2
""")
        Transfer.import_txt(transfers_txt, self.feed)
        transfer = Transfer.objects.get()  # Just one
        self.assertEqual(transfer.from_stop, self.stop1)
        self.assertEqual(transfer.to_stop, self.stop2)

    def test_import_transfers_txt_maximal(self):
        transfers_txt = StringIO("""\
from_stop_id,to_stop_id,transfer_type,min_transfer_time
STOP1,STOP2,2,5
""")
        Transfer.import_txt(transfers_txt, self.feed)
        transfer = Transfer.objects.get()
        self.assertEqual(transfer.from_stop, self.stop1)
        self.assertEqual(transfer.to_stop, self.stop2)
        self.assertEqual(transfer.transfer_type, 2)
        self.assertEqual(transfer.min_transfer_time, 5)

    def test_import_transfers_txt_omitted(self):
        transfers_txt = StringIO("""\
from_stop_id,to_stop_id,transfer_type,min_transfer_time
STOP1,STOP2,,
""")
        Transfer.import_txt(transfers_txt, self.feed)
        transfer = Transfer.objects.get()
        self.assertEqual(transfer.from_stop, self.stop1)
        self.assertEqual(transfer.to_stop, self.stop2)
        self.assertEqual(transfer.transfer_type, 0)
        self.assertEqual(transfer.min_transfer_time, None)

    def test_export_transfers_empty(self):
        transfers_txt = Transfer.export_txt(self.feed)
        self.assertFalse(transfers_txt)

    def test_export_transfers_minimal(self):
        Transfer.objects.create(
            from_stop=self.stop1, to_stop=self.stop2)
        transfers_txt = Transfer.export_txt(self.feed)
        self.assertEqual(transfers_txt, """\
from_stop_id,to_stop_id,transfer_type
STOP1,STOP2,0
""")

    def test_export_transfers_maximal(self):
        Transfer.objects.create(
            from_stop=self.stop1, to_stop=self.stop2, transfer_type=2,
            min_transfer_time=5)
        transfers_txt = Transfer.export_txt(self.feed)
        self.assertEqual(transfers_txt, """\
from_stop_id,to_stop_id,transfer_type,min_transfer_time
STOP1,STOP2,2,5
""")

    def test_export_transfers_two(self):
        Transfer.objects.create(
            from_stop=self.stop2, to_stop=self.stop1)
        Transfer.objects.create(
            from_stop=self.stop1, to_stop=self.stop2, transfer_type=2,
            min_transfer_time=5)
        transfers_txt = Transfer.export_txt(self.feed)
        self.assertEqual(transfers_txt, """\
from_stop_id,to_stop_id,transfer_type,min_transfer_time
STOP1,STOP2,2,5
STOP2,STOP1,0,
""")
