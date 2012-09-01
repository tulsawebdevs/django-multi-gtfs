import StringIO

from django.test import TestCase

from multigtfs.models import Feed, Shape, ShapePoint
from multigtfs.models.shape import import_shapes_txt


class ShapeTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create()

    def test_string(self):
        shape = Shape.objects.create(feed=self.feed, shape_id='S1')
        self.assertEqual(str(shape), '1-S1')
        shape_pt = ShapePoint.objects.create(shape=shape,
            lat='36.425288', lon='-117.133162', sequence=1)
        self.assertEqual(str(shape_pt), '1-S1-1')

    def test_import_shape_minimal(self):
        shape_txt = StringIO.StringIO("""\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
S1,36.425288,-117.133162,1
""")
        import_shapes_txt(shape_txt, self.feed)
        shape = Shape.objects.get()
        self.assertEqual(shape.feed, self.feed)
        self.assertEqual(shape.shape_id, 'S1')
        shape_pt = ShapePoint.objects.get()
        self.assertEqual(shape_pt.shape, shape)
        self.assertEqual(str(shape_pt.lat), '36.425288')
        self.assertEqual(str(shape_pt.lon), '-117.133162')
        self.assertEqual(shape_pt.sequence, 1)
        self.assertEqual(shape_pt.traveled, None)

    def test_import_shape_maximal(self):
        shape_txt = StringIO.StringIO("""\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
S1,36.425288,-117.133162,1,0
""")
        import_shapes_txt(shape_txt, self.feed)
        shape = Shape.objects.get()
        self.assertEqual(shape.feed, self.feed)
        self.assertEqual(shape.shape_id, 'S1')
        shape_pt = ShapePoint.objects.get()
        self.assertEqual(shape_pt.shape, shape)
        self.assertEqual(str(shape_pt.lat), '36.425288')
        self.assertEqual(str(shape_pt.lon), '-117.133162')
        self.assertEqual(shape_pt.sequence, 1)
        self.assertEqual(shape_pt.traveled, 0)

    def test_import_shape_traveled_omitted(self):
        shape_txt = StringIO.StringIO("""\
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
S1,36.425288,-117.133162,1,
""")
        import_shapes_txt(shape_txt, self.feed)
        shape = Shape.objects.get()
        self.assertEqual(shape.feed, self.feed)
        self.assertEqual(shape.shape_id, 'S1')
        shape_pt = ShapePoint.objects.get()
        self.assertEqual(shape_pt.shape, shape)
        self.assertEqual(str(shape_pt.lat), '36.425288')
        self.assertEqual(str(shape_pt.lon), '-117.133162')
        self.assertEqual(shape_pt.sequence, 1)
        self.assertEqual(shape_pt.traveled, None)
