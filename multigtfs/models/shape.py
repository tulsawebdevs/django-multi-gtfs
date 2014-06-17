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

"""
Define Shape model for rows in shapes.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

trips.txt is optional

- shape_id (required)
The shape_id field contains an ID that uniquely identifies a shape.

- shape_pt_lat (required)
The shape_pt_lat field associates a shape point's latitude with a shape ID.
The field value must be a valid WGS 84 latitude. Each row in shapes.txt
represents a shape point in your shape definition.

For example, if the shape "A_shp" has three points in its definition, the
shapes.txt file might contain these rows to define the shape:

    A_shp,37.61956,-122.48161,0
    A_shp,37.64430,-122.41070,6
    A_shp,37.65863,-122.30839,11

- shape_pt_lon (required)
The shape_pt_lon field associates a shape point's longitude with a shape ID.
The field value must be a valid WGS 84 longitude value from -180 to 180. Each
row in shapes.txt represents a shape point in your shape definition.

For example, if the shape "A_shp" has three points in its definition, the
shapes.txt file might contain these rows to define the shape:

    A_shp,37.61956,-122.48161,0
    A_shp,37.64430,-122.41070,6
    A_shp,37.65863,-122.30839,11

- shape_pt_sequence (required)
The shape_pt_sequence field associates the latitude and longitude of a shape
point with its sequence order along the shape. The values for shape_pt_sequence
must be non-negative integers, and they must increase along the trip.

For example, if the shape "A_shp" has three points in its definition, the
shapes.txt file might contain these rows to define the shape:

    A_shp,37.61956,-122.48161,0
    A_shp,37.64430,-122.41070,6
    A_shp,37.65863,-122.30839,11

- shape_dist_traveled (optional)
When used in the shapes.txt file, the shape_dist_traveled field positions a
shape point as a distance traveled along a shape from the first shape point.
The shape_dist_traveled field represents a real distance traveled along the
route in units such as feet or kilometers. This information allows the trip
planner to determine how much of the shape to draw when showing part of a trip
on the map. The values used for shape_dist_traveled must increase along with
shape_pt_sequence: they cannot be used to show reverse travel along a route.

The units used for shape_dist_traveled in the shapes.txt file must match the
units that are used for this field in the stop_times.txt file.

For example, if a bus travels along the three points defined above for A_shp,
the additional shape_dist_traveled values (shown here in kilometers) would look
like this:

    A_shp,37.61956,-122.48161,0,0
    A_shp,37.64430,-122.41070,6,6.8310
    A_shp,37.65863,-122.30839,11,15.8765
"""
from __future__ import unicode_literals
import warnings

from django.contrib.gis.geos import LineString
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Shape(Base):
    """The path the vehicle takes along the route"""
    feed = models.ForeignKey('Feed')
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
    shape = models.ForeignKey('Shape', related_name='points')
    point = models.PointField(
        help_text='WGS 84 latitude/longitude of shape point')
    sequence = models.IntegerField()
    traveled = models.FloatField(
        null=True, blank=True,
        help_text='Distance of point from start of shape')

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
