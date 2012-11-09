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

import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Fare, FareRule, Route, Zone


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

    def test_import_fare_rules_txt_route(self):
        fare_rules_txt = StringIO.StringIO("""\
fare_id,route_id,origin_id,destination_id,contains_id
p,AB,,,
""")
        route = Route.objects.create(feed=self.feed, route_id='AB', rtype=3)
        FareRule.import_txt(fare_rules_txt, self.feed)
        fr = FareRule.objects.get()
        self.assertEqual(fr.fare, self.fare)
        self.assertEqual(fr.route, route)
        self.assertEqual(fr.origin, None)
        self.assertEqual(fr.destination, None)
        self.assertEqual(fr.contains, None)

    def test_import_fare_rules_txt_origin(self):
        fare_rules_txt = StringIO.StringIO("""\
fare_id,route_id,origin_id
p,,2
""")
        zone = Zone.objects.create(feed=self.feed, zone_id='2')
        FareRule.import_txt(fare_rules_txt, self.feed)
        fr = FareRule.objects.get()
        self.assertEqual(fr.fare, self.fare)
        self.assertEqual(fr.route, None)
        self.assertEqual(fr.origin, zone)
        self.assertEqual(fr.destination, None)
        self.assertEqual(fr.contains, None)

    def test_import_fare_rules_txt_full(self):
        fare_rules_txt = StringIO.StringIO("""\
fare_id,route_id,origin_id,destination_id,contains_id
p,AB,1,2,12
""")
        route = Route.objects.create(feed=self.feed, route_id='AB', rtype=3)
        zone1 = Zone.objects.create(feed=self.feed, zone_id='1')
        zone2 = Zone.objects.create(feed=self.feed, zone_id='2')
        zone12 = Zone.objects.create(feed=self.feed, zone_id='12')
        FareRule.import_txt(fare_rules_txt, self.feed)
        fr = FareRule.objects.get()
        self.assertEqual(fr.fare, self.fare)
        self.assertEqual(fr.route, route)
        self.assertEqual(fr.origin, zone1)
        self.assertEqual(fr.destination, zone2)
        self.assertEqual(fr.contains, zone12)

    def test_export_fare_rules_empty(self):
        fare_rules_txt = FareRule.objects.in_feed(self.feed).export_txt()
        self.assertFalse(fare_rules_txt)

    def test_export_fare_rules_degraded(self):
        # This is possible, but pointless
        FareRule.objects.create(fare=self.fare)
        fare_rules_txt = FareRule.objects.in_feed(self.feed).export_txt()
        self.assertEqual(fare_rules_txt, '''\
fare_id
p
''')

    def test_export_fare_rules_route_id(self):
        route = Route.objects.create(feed=self.feed, route_id='AB', rtype=3)
        FareRule.objects.create(fare=self.fare, route=route)
        fare_rules_txt = FareRule.objects.in_feed(self.feed).export_txt()
        self.assertEqual(fare_rules_txt, '''\
fare_id,route_id
p,AB
''')

    def test_export_fare_rules_contains(self):
        zone12 = Zone.objects.create(feed=self.feed, zone_id='12')
        FareRule.objects.create(fare=self.fare, contains=zone12)
        fare_rules_txt = FareRule.objects.in_feed(self.feed).export_txt()
        self.assertEqual(fare_rules_txt, '''\
fare_id,contains_id
p,12
''')

    def test_export_fare_rules_complete(self):
        route = Route.objects.create(feed=self.feed, route_id='AB', rtype=3)
        zone1 = Zone.objects.create(feed=self.feed, zone_id='1')
        zone2 = Zone.objects.create(feed=self.feed, zone_id='2')
        zone12 = Zone.objects.create(feed=self.feed, zone_id='12')
        FareRule.objects.create(
            fare=self.fare, route=route, origin=zone1, destination=zone2,
            contains=zone12)
        fare_rules_txt = FareRule.objects.in_feed(self.feed).export_txt()
        self.assertEqual(fare_rules_txt, '''\
fare_id,route_id,origin_id,destination_id,contains_id
p,AB,1,2,12
''')
