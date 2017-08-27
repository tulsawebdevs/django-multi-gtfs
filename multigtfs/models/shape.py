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
import warnings

from django.contrib.gis.geos import LineString
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Shape(Base):
    """The path the vehicle takes along the route.

    Implements shapes.txt."""
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    shape_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for a shape.")
    geometry = models.LineStringField(
        null=True, blank=True,
        help_text='Geometry cache of ShapePoints')

    def __str__(self):
        return "%d-%s" % (self.feed.id, self.shape_id)

    def update_geometry(self, update_parent=True):
        """Update the geometry from the related ShapePoints"""
        original = self.geometry
        points = self.points.order_by(
            'sequence').values_list('point', flat=True)
        if len(points) > 1:
            self.geometry = LineString([pt.coords for pt in points])
            if self.geometry != original:
                self.save()
                if update_parent:
                    for trip in self.trip_set.all():
                        trip.update_geometry()

    class Meta:
        db_table = 'shape'
        app_label = 'multigtfs'

    _rel_to_feed = 'feed'


@python_2_unicode_compatible
class ShapePoint(Base):
    """A point along the shape"""
    shape = models.ForeignKey(
        'Shape', on_delete=models.CASCADE, related_name='points')
    point = models.PointField(
        help_text='WGS 84 latitude/longitude of shape point')
    sequence = models.IntegerField()
    traveled = models.FloatField(
        null=True, blank=True,
        help_text='Distance of point from start of shape')
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "%s-%d" % (self.shape, self.sequence)

    def getlon(self):
        return self.point[0] if self.point else 0.0

    def setlon(self, value):
        if self.point:
            self.point[0] = value
        else:
            self.point = "POINT(%s 0)" % value

    lon = property(getlon, setlon, doc="WGS 84 longitude of shape point")

    def getlat(self):
        return self.point[1] if self.point else 0.0

    def setlat(self, value):
        if self.point:
            self.point[1] = value
        else:
            self.point = "POINT(0 %s)" % value

    lat = property(getlat, setlat, doc="WGS 84 latitude of shape point")

    def __init__(self, *args, **kwargs):
        """Initialize a ShapePoint

        If the legacy lat and lon params are used, then warn and initialize
        the point from them.
        """
        lat = kwargs.pop('lat', None)
        lon = kwargs.pop('lon', None)
        if lat is not None or lon is not None:
            assert kwargs.get('point') is None
            msg = "Setting ShapePoint location with lat and lon is deprecated"
            warnings.warn(msg, DeprecationWarning)
            kwargs['point'] = "POINT(%s %s)" % (lon or 0.0, lat or 0.0)

        super(ShapePoint, self).__init__(*args, **kwargs)

    class Meta:
        db_table = 'shape_point'
        app_label = 'multigtfs'

    _column_map = (
        ('shape_id', 'shape__shape_id'),
        ('shape_pt_lat', 'point[1]'),
        ('shape_pt_lon', 'point[0]'),
        ('shape_pt_sequence', 'sequence'),
        ('shape_dist_traveled', 'traveled')
    )
    _filename = 'shapes.txt'
    _rel_to_feed = 'shape__feed'
    _sort_order = ('shape__shape_id', 'sequence')
    _unique_fields = ('shape_id', 'shape_pt_sequence')


@receiver(post_save, sender=ShapePoint, dispatch_uid="post_save_shapepoint")
def post_save_shapepoint(sender, instance, **kwargs):
    '''Update related objects when the ShapePoint is updated'''
    instance.shape.update_geometry()
