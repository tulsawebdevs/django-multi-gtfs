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

from django.contrib.gis.geos import MultiLineString
from django.test import TestCase
from django.utils.six import StringIO

from multigtfs.models import Feed, Route, Shape, ShapePoint, Trip


class ShapeTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        shape = Shape.objects.create(feed=self.feed, shape_id='S1')
        self.assertEqual(str(shape), '%d-S1' % self.feed.id)
        shape_pt = ShapePoint.objects.create(
            shape=shape, point="POINT(-117.133162 36.425288)", sequence=1)
        self.assertEqual(str(shape_pt), '%d-S1-1' % self.feed.id)

    def test_legacy_lat_long(self):
        shape = Shape.objects.create(feed=self.feed, shape_id='s1')
        shape_pt1 = ShapePoint(shape=shape, sequence=1)
        shape_pt1.lat = 36.425288
        shape_pt1.lon = -117.133162
        shape_pt1.save()
        shape_pt2 = ShapePoint(shape=shape, sequence=2)
        shape_pt2.lon = -117.14
        shape_pt2.lat = 36.43
        shape_pt2.save()
        self.assertEqual(shape_pt1.point.coords, (-117.133162, 36.425288))
        self.assertEqual(shape_pt1.lat, 36.425288)
        self.assertEqual(shape_pt1.lon, -117.133162)
        self.assertEqual(shape_pt2.point.coords, (-117.14, 36.43))
        self.assertEqual(shape_pt2.lat, 36.43)
        self.assertEqual(shape_pt2.lon, -117.14)

    def test_legacy_create_with_lat_lon(self):
        shape = Shape.objects.create(feed=self.feed, shape_id='S1')
        shape_pt = ShapePoint.objects.create(
            shape=shape, lat='36.425288', lon='-117.133162', sequence=1)
        self.assertEqual(shape_pt.point.coords, (-117.133162, 36.425288))

    def test_import_shape_minimal(self):
        shape_txt = StringIO("""\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
S1,36.425288,-117.133162,1
""")
        ShapePoint.import_txt(shape_txt, self.feed)
        shape = Shape.objects.get()
        self.assertEqual(shape.feed, self.feed)
        self.assertEqual(shape.shape_id, 'S1')
        self.assertEqual(shape.geometry, None)
        shape_pt = ShapePoint.objects.get()
        self.assertEqual(shape_pt.shape, shape)
        self.assertEqual(shape_pt.point.coords, (-117.133162, 36.425288))
        self.assertEqual(shape_pt.sequence, 1)
        self.assertEqual(shape_pt.traveled, None)

    def test_import_shape_duplicate(self):
        shape_txt = StringIO("""\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
S1,36.425288,-117.133162,1
S1,36.42,-117.13,1
S1,36.43,-117.14,2
""")
        ShapePoint.import_txt(shape_txt, self.feed)
        shape = Shape.objects.get()  # Just one
        self.assertEqual(shape.feed, self.feed)
        self.assertEqual(shape.shape_id, 'S1')
        self.assertEqual(2, ShapePoint.objects.count())
        shape_pt, shape_pt2 = ShapePoint.objects.order_by('sequence')
        self.assertEqual(shape_pt.shape, shape)
        self.assertEqual(shape_pt.point.coords, (-117.133162, 36.425288))
        self.assertEqual(shape_pt.sequence, 1)
        self.assertEqual(shape_pt2.shape, shape)
        self.assertEqual(shape_pt2.point.coords, (-117.14, 36.43))
        self.assertEqual(shape_pt2.sequence, 2)

    def test_import_shape_maximal(self):
        shape_txt = StringIO("""\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
S1,36.425288,-117.133162,1,0
""")
        ShapePoint.import_txt(shape_txt, self.feed)
        shape = Shape.objects.get()
        self.assertEqual(shape.feed, self.feed)
        self.assertEqual(shape.shape_id, 'S1')
        self.assertEqual(shape.geometry, None)
        shape_pt = ShapePoint.objects.get()
        self.assertEqual(shape_pt.shape, shape)
        self.assertEqual(shape_pt.point.coords, (-117.133162, 36.425288))
        self.assertEqual(shape_pt.sequence, 1)
        self.assertEqual(shape_pt.traveled, 0)

    def test_import_shape_traveled_omitted(self):
        shape_txt = StringIO("""\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
S1,36.425288,-117.133162,1,
""")
        ShapePoint.import_txt(shape_txt, self.feed)
        shape = Shape.objects.get()
        self.assertEqual(shape.feed, self.feed)
        self.assertEqual(shape.shape_id, 'S1')
        self.assertEqual(shape.geometry, None)
        shape_pt = ShapePoint.objects.get()
        self.assertEqual(shape_pt.shape, shape)
        self.assertEqual(shape_pt.point.coords, (-117.133162, 36.425288))
        self.assertEqual(shape_pt.sequence, 1)
        self.assertEqual(shape_pt.traveled, None)

    def test_export_shape_empty(self):
        shape_txt = ShapePoint.export_txt(self.feed)
        self.assertFalse(shape_txt)

    def test_export_shape_minimal(self):
        shape = Shape.objects.create(feed=self.feed, shape_id='S1')
        ShapePoint.objects.create(
            shape=shape, point="POINT(-117.133162 36.425288)", sequence=1)
        shape_txt = ShapePoint.export_txt(self.feed)
        self.assertEqual(shape_txt, """\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
S1,36.425288,-117.133162,1
""")

    def test_export_shape_maximal(self):
        shape = Shape.objects.create(feed=self.feed, shape_id='S1')
        ShapePoint.objects.create(
            shape=shape, point="POINT(-117.133162 36.425288)", sequence=1,
            traveled=1.1)
        shape_txt = ShapePoint.export_txt(self.feed)
        self.assertEqual(shape_txt, """\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
S1,36.425288,-117.133162,1,1.1
""")

    def test_update_geometry_on_shapepoint_save(self):
        shape = Shape.objects.create(feed=self.feed)
        route = Route.objects.create(feed=self.feed, rtype=3)
        trip = Trip.objects.create(shape=shape, route=route)
        ShapePoint.objects.create(
            shape=shape, point="POINT(-117.133162 36.425288)", sequence=1)
        ShapePoint.objects.create(
            shape=shape, point="POINT(-117.13 36.42)", sequence=2)

        shape = Shape.objects.get(id=shape.id)
        trip = Trip.objects.get(id=trip.id)
        route = Route.objects.get(id=route.id)
        self.assertEqual(
            shape.geometry.coords,
            ((-117.133162, 36.425288), (-117.13, 36.42)))
        self.assertEqual(trip.geometry, shape.geometry)
        self.assertEqual(route.geometry,
                         MultiLineString(shape.geometry, srid=4326))

    def test_update_geometry_no_parent(self):
        shape = Shape.objects.create(feed=self.feed)
        route = Route.objects.create(feed=self.feed, rtype=3)
        trip = Trip.objects.create(shape=shape, route=route)
        ShapePoint.objects.create(
            shape=shape, point="POINT(-117.133162 36.425288)", sequence=1)
        ShapePoint.objects.create(
            shape=shape, point="POINT(-117.13 36.42)", sequence=2)

        shape.geometry = None
        shape.save()
        trip.geometry = None
        trip.save()
        shape.update_geometry(update_parent=False)

        shape = Shape.objects.get(id=shape.id)
        trip = Trip.objects.get(id=trip.id)
        self.assertEqual(
            shape.geometry.coords,
            ((-117.133162, 36.425288), (-117.13, 36.42)))
        self.assertIsNone(trip.geometry, None)

    def test_shape_geometry_is_ordered(self):
        '''Shape geometry is ordered by ShapePoint sequence

        See issue #24
        '''
        shape = Shape.objects.create(feed=self.feed)
        shape.points.create(point="POINT(-117.2 36.42)", sequence=2)
        shape.points.create(point="POINT(-117.6 36.42)", sequence=6)
        shape.points.create(point="POINT(-117.7 36.42)", sequence=7)
        shape.points.create(point="POINT(-117.3 36.42)", sequence=3)
        shape.points.create(point="POINT(-117.8 36.42)", sequence=8)
        shape.points.create(point="POINT(-117.1 36.42)", sequence=1)
        shape.points.create(point="POINT(-117.4 36.42)", sequence=4)
        shape.points.create(point="POINT(-117.9 36.42)", sequence=9)
        shape.points.create(point="POINT(-117.5 36.42)", sequence=5)
        self.assertEqual(
            shape.geometry.coords,
            ((-117.1, 36.42), (-117.2, 36.42), (-117.3, 36.42),
             (-117.4, 36.42), (-117.5, 36.42), (-117.6, 36.42),
             (-117.7, 36.42), (-117.8, 36.42), (-117.9, 36.42)))
