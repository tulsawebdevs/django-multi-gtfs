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

from csv import DictReader

from django.db import models


class Shape(models.Model):
    """The path the vehicle takes along the route"""
    feed = models.ForeignKey('Feed')
    shape_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for a shape.")

    def __unicode__(self):
        return u"%d-%s" % (self.feed.id, self.shape_id)

    class Meta:
        db_table = 'shape'
        app_label = 'multigtfs'


class ShapePoint(models.Model):
    """A point along the shape"""
    shape = models.ForeignKey('Shape', related_name='points')
    lat = models.DecimalField('Latitude',
        max_digits=13, decimal_places=8,
        help_text='WGS 84 latitude of shape point')
    lon = models.DecimalField('Longitude',
        max_digits=13, decimal_places=8,
        help_text='WGS 84 longtitude of shape point')
    sequence = models.IntegerField()
    traveled = models.FloatField(
        null=True,
        help_text='Distance of point from start of shape')

    def __unicode__(self):
        return u"%s-%d" % (self.shape, self.sequence)

    class Meta:
        db_table = 'shape_point'
        app_label = 'multigtfs'


def import_shapes_txt(shapes_file, feed):
    """Import shapes.txt into Shape records for feed

    Keyword arguments:
    shapes_file -- A open shapes.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(shapes_file)
    name_map = dict(shape_pt_lat='lat', shape_pt_lon='lon',
                    shape_pt_sequence='sequence',
                    shape_dist_traveled='traveled')
    for row in reader:
        shape_id = row.pop('shape_id')
        shape, _c = Shape.objects.get_or_create(feed=feed, shape_id=shape_id)
        fields = dict((name_map.get(k, k), v) for k, v in row.items())
        # Force empty strings to None
        traveled = fields.get('traveled', None)
        fields['traveled'] = traveled or None
        ShapePoint.objects.create(shape=shape, **fields)
