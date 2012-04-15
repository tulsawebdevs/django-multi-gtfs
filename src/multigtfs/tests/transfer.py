import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Stop, Transfer
from multigtfs.models.transfer import import_transfers_txt


class TransferTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.stop1 = Stop.objects.create(
            feed=self.feed, stop_id='STOP1', lat="36.4", lon="-117.1")
        self.stop2 = Stop.objects.create(
            feed=self.feed, stop_id='STOP2', lat="36.5", lon="-117.2")

    def test_string(self):
        transfer = Transfer.objects.create(
            from_stop=self.stop1, to_stop=self.stop2)
        self.assertEqual(str(transfer), '1-STOP1-STOP2')

    def test_import_transfers_txt_minimal(self):
        transfers_txt = StringIO.StringIO("""\
from_stop_id,to_stop_id
STOP1,STOP2
""")
        import_transfers_txt(transfers_txt, self.feed)
        transfer = Transfer.objects.get()
        self.assertEqual(transfer.from_stop, self.stop1)
        self.assertEqual(transfer.to_stop, self.stop2)
        self.assertEqual(transfer.transfer_type, 0)
        self.assertEqual(transfer.min_transfer_time, None)

    def test_import_transfers_txt_maximal(self):
        transfers_txt = StringIO.StringIO("""\
from_stop_id,to_stop_id,transfer_type,min_transfer_time
STOP1,STOP2,2,5
""")
        import_transfers_txt(transfers_txt, self.feed)
        transfer = Transfer.objects.get()
        self.assertEqual(transfer.from_stop, self.stop1)
        self.assertEqual(transfer.to_stop, self.stop2)
        self.assertEqual(transfer.transfer_type, 2)
        self.assertEqual(transfer.min_transfer_time, 5)

    def test_import_transfers_txt_omitted(self):
        transfers_txt = StringIO.StringIO("""\
from_stop_id,to_stop_id,transfer_type,min_transfer_time
STOP1,STOP2,,
""")
        import_transfers_txt(transfers_txt, self.feed)
        transfer = Transfer.objects.get()
        self.assertEqual(transfer.from_stop, self.stop1)
        self.assertEqual(transfer.to_stop, self.stop2)
        self.assertEqual(transfer.transfer_type, 0)
        self.assertEqual(transfer.min_transfer_time, None)
