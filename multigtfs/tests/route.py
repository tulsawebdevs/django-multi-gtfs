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

from multigtfs.models import Feed, Agency, Route


class RouteTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        route = Route.objects.create(feed=self.feed, route_id='RTEST', rtype=3)
        self.assertEqual(str(route), '1-RTEST')

    def test_import_routes_txt_minimal(self):
        routes_txt = StringIO.StringIO("""\
route_id,route_short_name,route_long_name,route_type
AB,10,Airport - Bullfrog,3
""")
        Route.import_txt(routes_txt, self.feed)
        route = Route.objects.get()
        self.assertEqual(route.feed, self.feed)
        self.assertEqual(route.route_id, 'AB')
        self.assertEqual(route.agency, None)
        self.assertEqual(route.short_name, '10')
        self.assertEqual(route.long_name, 'Airport - Bullfrog')
        self.assertEqual(route.desc, '')
        self.assertEqual(route.rtype, 3)
        self.assertEqual(route.url, '')
        self.assertEqual(route.color, '')
        self.assertEqual(route.text_color, '')

    def test_import_routes_txt_maximal(self):
        routes_txt = StringIO.StringIO("""\
route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,\
route_url,route_color,route_text_color
AB,DTA,10,Airport - Bullfrog,"Our Airport Route", 3,http://example.com,\
00FFFF,000000
""")
        agency = Agency.objects.create(feed=self.feed, agency_id='DTA')
        Route.import_txt(routes_txt, self.feed)
        route = Route.objects.get()
        self.assertEqual(route.feed, self.feed)
        self.assertEqual(route.route_id, 'AB')
        self.assertEqual(route.agency, agency)
        self.assertEqual(route.short_name, '10')
        self.assertEqual(route.long_name, 'Airport - Bullfrog')
        self.assertEqual(route.desc, 'Our Airport Route')
        self.assertEqual(route.rtype, 3)
        self.assertEqual(route.url, 'http://example.com')
        self.assertEqual(route.color, '00FFFF')
        self.assertEqual(route.text_color, '000000')

    def test_export_routes_txt_none(self):
        routes_txt = Route.objects.in_feed(self.feed).export_txt()
        self.assertFalse(routes_txt)

    def test_export_routes_txt_minimal(self):
        Route.objects.create(
            feed=self.feed, route_id='AB', short_name='10',
            long_name='Airport - Bullfrog', rtype=3)
        routes_txt = Route.objects.in_feed(self.feed).export_txt()
        self.assertEquals(routes_txt, """\
route_id,route_short_name,route_long_name,route_type
AB,10,Airport - Bullfrog,3
""")

    def test_export_routes_txt_maximal(self):
        agency = Agency.objects.create(feed=self.feed, agency_id='DTA')
        Route.objects.create(
            feed=self.feed, agency=agency, route_id='AB', short_name='10',
            long_name='Airport - Bullfrog', desc='Our Airport Route',
            rtype=3, url='http://example.com', color='00FFFF',
            text_color='000000')
        routes_txt = Route.objects.in_feed(self.feed).export_txt()
        self.assertEquals(routes_txt, """\
route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,\
route_url,route_color,route_text_color
AB,DTA,10,Airport - Bullfrog,Our Airport Route,3,http://example.com,\
00FFFF,000000
""")
