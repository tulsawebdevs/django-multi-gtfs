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

from multigtfs.models import Feed, Agency, Route, Trip


class RouteTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        route = Route.objects.create(feed=self.feed, route_id='RTEST', rtype=3)
        self.assertEqual(str(route), '%d-RTEST' % self.feed.id)

    def test_import_routes_txt_minimal(self):
        routes_txt = StringIO("""\
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

    def test_import_routes_txt_duplicate(self):
        routes_txt = StringIO("""\
route_id,route_short_name,route_long_name,route_type
AB,10,Airport - Bullfrog,3
AB,11,Airport Party Bus,3
""")
        Route.import_txt(routes_txt, self.feed)
        route = Route.objects.get()  # Just one
        self.assertEqual(route.feed, self.feed)
        self.assertEqual(route.route_id, 'AB')
        self.assertEqual(route.short_name, '10')

    def test_import_routes_txt_maximal(self):
        routes_txt = StringIO("""\
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
        routes_txt = Route.export_txt(self.feed)
        self.assertFalse(routes_txt)

    def test_export_routes_txt_minimal(self):
        Route.objects.create(
            feed=self.feed, route_id='AB', short_name='10',
            long_name='Airport - Bullfrog', rtype=3)
        routes_txt = Route.export_txt(self.feed)
        self.assertEqual(routes_txt, """\
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
        routes_txt = Route.export_txt(self.feed)
        self.assertEqual(routes_txt, """\
route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,\
route_url,route_color,route_text_color
AB,DTA,10,Airport - Bullfrog,Our Airport Route,3,http://example.com,\
00FFFF,000000
""")

    def test_update_geometry_no_trips(self):
        route = Route.objects.create(feed=self.feed, route_id='RTEST', rtype=3)
        self.assertFalse(route.geometry)
        route.update_geometry()
        self.assertFalse(route.geometry)

    def test_update_geometry_1_trip(self):
        route = Route.objects.create(feed=self.feed, route_id='RTEST', rtype=3)
        Trip.objects.create(route=route, geometry='LINESTRING(1 2, 1 3)')
        self.assertFalse(route.geometry)
        route.update_geometry()
        self.assertEqual(route.geometry.coords, (((1.0, 2.0), (1.0, 3.0)),))

    def test_update_geometry_2_trips_different_geometries(self):
        route = Route.objects.create(feed=self.feed, route_id='RTEST', rtype=3)
        Trip.objects.create(route=route, geometry='LINESTRING(1 2, 1 3)')
        Trip.objects.create(route=route, geometry='LINESTRING(1 2, 1 4)')
        self.assertFalse(route.geometry)
        route.update_geometry()
        route_coords = list(route.geometry.coords)
        route_coords.sort()
        self.assertEqual(len(route_coords), 2)
        self.assertEqual(
            route_coords,
            [((1., 2.), (1., 3.)), ((1., 2.), (1., 4.))])

    def test_update_geometry_2_trips_same_geometry(self):
        route = Route.objects.create(feed=self.feed, route_id='RTEST', rtype=3)
        Trip.objects.create(route=route, geometry='LINESTRING(1 2, 1 3)')
        Trip.objects.create(route=route, geometry='LINESTRING(1 2, 1 3)')
        self.assertFalse(route.geometry)
        route.update_geometry()
        route_coords = list(route.geometry.coords)
        route_coords.sort()
        self.assertEqual(len(route_coords), 1)
        self.assertEqual(route.geometry.coords, (((1.0, 2.0), (1.0, 3.0)),))

    def test_update_geometry_no_change(self):
        # For code coverage
        route = Route.objects.create(
            feed=self.feed, route_id='RTEST', rtype=3,
            geometry='MULTILINESTRING((1 2, 1 3))')
        Trip.objects.create(route=route, geometry='LINESTRING(1 2, 1 3)')
        self.assertEqual(route.geometry.coords, (((1.0, 2.0), (1.0, 3.0)),))
        route.update_geometry()
        self.assertEqual(route.geometry.coords, (((1.0, 2.0), (1.0, 3.0)),))
