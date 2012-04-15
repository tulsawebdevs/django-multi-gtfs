import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Fare, FareRule, Route, Zone
from multigtfs.utils import import_fare_rules


class FareRuleTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.fare = Fare.objects.create(
            feed=self.feed, fare_id='p', price='1.25', currency_type='USD')

    def test_string(self):
        fr = FareRule.objects.create(fare=self.fare)
        self.assertEqual(str(fr), '1-p')
        route = Route.objects.create(feed=self.feed, route_id='R1', rtype=3)
        fr.route = route
        self.assertEqual(str(fr), '1-p-R1')

    def test_import_fare_rules_route(self):
        fare_rules_txt = StringIO.StringIO("""\
fare_id,route_id,origin_id,destination_id,contains_id
p,AB,,,
""")
        route = Route.objects.create(feed=self.feed, route_id='AB', rtype=3)
        import_fare_rules(fare_rules_txt, self.feed)
        fr = FareRule.objects.get()
        self.assertEqual(fr.fare, self.fare)
        self.assertEqual(fr.route, route)
        self.assertEqual(fr.origin, None)
        self.assertEqual(fr.destination, None)
        self.assertEqual(fr.contains, None)

    def test_import_fare_rules_origin(self):
        fare_rules_txt = StringIO.StringIO("""\
fare_id,route_id,origin_id
p,,2
""")
        zone = Zone.objects.create(feed=self.feed, zone_id='2')
        import_fare_rules(fare_rules_txt, self.feed)
        fr = FareRule.objects.get()
        self.assertEqual(fr.fare, self.fare)
        self.assertEqual(fr.route, None)
        self.assertEqual(fr.origin, zone)
        self.assertEqual(fr.destination, None)
        self.assertEqual(fr.contains, None)

    def test_import_fare_rules_full(self):
        fare_rules_txt = StringIO.StringIO("""\
fare_id,route_id,origin_id,destination_id,contains_id
p,AB,1,2,12
""")
        route = Route.objects.create(feed=self.feed, route_id='AB', rtype=3)
        zone1 = Zone.objects.create(feed=self.feed, zone_id='1')
        zone2 = Zone.objects.create(feed=self.feed, zone_id='2')
        zone12 = Zone.objects.create(feed=self.feed, zone_id='12')
        import_fare_rules(fare_rules_txt, self.feed)
        fr = FareRule.objects.get()
        self.assertEqual(fr.fare, self.fare)
        self.assertEqual(fr.route, route)
        self.assertEqual(fr.origin, zone1)
        self.assertEqual(fr.destination, zone2)
        self.assertEqual(fr.contains, zone12)
