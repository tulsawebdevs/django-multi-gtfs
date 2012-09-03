import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Fare


class FareTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        fa = Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD',
            payment_method=0, transfers=0)
        self.assertEqual(str(fa), '1-p(1.25 USD)')

    def test_import_fare_attributes_minimal(self):
        fare_attributes_txt = StringIO.StringIO("""\
fare_id,price,currency_type,payment_method,transfers
p,1.25,USD,0,0
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()
        self.assertEqual(fa.feed, self.feed)
        self.assertEqual(fa.fare_id, 'p')
        self.assertEqual(str(fa.price), '1.25')
        self.assertEqual(fa.currency_type, 'USD')
        self.assertEqual(fa.payment_method, 0)
        self.assertEqual(fa.transfers, 0)
        self.assertEqual(fa.transfer_duration, None)

    def test_import_fare_attributes_maximal(self):
        fare_attributes_txt = StringIO.StringIO("""\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,1.25,USD,0,0,60
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()
        self.assertEqual(fa.transfer_duration, 60)

    def test_import_fare_attributes_omitted(self):
        fare_attributes_txt = StringIO.StringIO("""\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,1.25,USD,0,0
""")
        Fare.import_txt(fare_attributes_txt, self.feed)
        fa = Fare.objects.get()
        self.assertEqual(fa.fare_id, 'p')
        self.assertEqual(fa.transfer_duration, None)

    def test_export_fare_attributes_minimal(self):
        Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD',
            payment_method=0, transfers=0)
        fare_txt = Fare.objects.in_feed(self.feed).export_txt()
        self.assertEqual(fare_txt, """\
fare_id,price,currency_type,payment_method,transfers
p,1.25,USD,0,0
""")

    def test_export_fare_attributes_maximal(self):
        Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD',
            payment_method=0, transfers=0, transfer_duration=3600)
        fare_txt = Fare.objects.in_feed(self.feed).export_txt()
        self.assertEqual(fare_txt, """\
fare_id,price,currency_type,payment_method,transfers,transfer_duration
p,1.25,USD,0,0,3600
""")
