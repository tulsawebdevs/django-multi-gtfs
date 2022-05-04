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

from multigtfs.models import Feed, Route, RouteDirection


class RouteDirectionTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()
        self.route = Route.objects.create(
            feed=self.feed, route_id='R1', rtype=3)

    def test_string(self):
        direction = RouteDirection.objects.create(
            route=self.route, direction='0',
            direction_name='Direction')
        self.assertEqual(str(direction), '%d-R1-0' % self.feed.id)

    def test_import_route_directions_txt(self):
        route_directions_txt = StringIO("""\
route_id,direction_id,direction_name
R1,0,Direction
""")
        RouteDirection.import_txt(route_directions_txt, self.feed)
        direction = RouteDirection.objects.get()
        self.assertEqual(direction.route, self.route)
        self.assertEqual(direction.direction, '0')
        self.assertEqual(direction.direction_name, 'Direction')

    def test_import_route_directions_txt_duplicate(self):
        route_directions_txt = StringIO("""\
route_id,direction_id,direction_name
R1,0,Direction
R1,0,Direction
""")
        RouteDirection.import_txt(route_directions_txt, self.feed)
        direction = RouteDirection.objects.get()
        self.assertEqual(direction.direction, '0')

    def test_export_route_directions_empty(self):
        directions_txt = RouteDirection.export_txt(self.feed)
        self.assertFalse(directions_txt)

    def test_export_route_directions_txt(self):
        RouteDirection.objects.create(
            route=self.route, direction='0',
            direction_name='Direction')
        directions_txt = RouteDirection.export_txt(self.feed)
        self.assertEqual(directions_txt, """\
route_id,direction_id,direction_name
R1,0,Direction
""")
