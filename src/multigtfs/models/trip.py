"""
Define Trip model for rows in trips.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

trips.txt is required

- route_id (required)
The route_id field contains an ID that uniquely identifies a route. This value
is referenced from the routes.txt file.

- service_id (required)
The service_id contains an ID that uniquely identifies a set of dates when
service is available for one or more routes. This value is referenced from the
calendar.txt or calendar_dates.txt file.

- trip_id (required)
The trip_id field contains an ID that identifies a trip. The trip_id is dataset
unique.

- trip_headsign (optional)
The trip_headsign field contains the text that appears on a sign that
identifies the trip's destination to passengers. Use this field to distinguish
between different patterns of service in the same route. If the headsign
changes during a trip, you can override the trip_headsign by specifying values
for the the stop_headsign field in stop_times.txt.

See a Google Maps screenshot highlighting the headsign:
  http://bit.ly/A3ot2j

- trip_short_name (optional)
The trip_short_name field contains the text that appears in schedules and sign
boards to identify the trip to passengers, for example, to identify train
numbers for commuter rail trips. If riders do not commonly rely on trip names,
please leave this field blank.

A trip_short_name value, if provided, should uniquely identify a trip within a
service day; it should not be used for destination names or limited/express
designations.

- direction_id (optional)
The direction_id field contains a binary value that indicates the direction of
travel for a trip. Use this field to distinguish between bi-directional trips
with the same route_id. This field is not used in routing; it provides a way to
separate trips by direction when publishing time tables. You can specify names
for each direction with the trip_headsign field.

    * 0 - travel in one direction (e.g. outbound travel)
    * 1 - travel in the opposite direction (e.g. inbound travel)

For example, you could use the trip_headsign and direction_id fields together
to assign a name to travel in each direction on trip "1234", the trips.txt file
would contain these rows for use in time tables:

    trip_id, ... ,trip_headsign,direction_id
    1234, ... , to Airport,0
    1505, ... , to Downtown,1

- block_id (optional)
The block_id field identifies the block to which the trip belongs. A block
consists of two or more sequential trips made using the same vehicle, where a
passenger can transfer from one trip to the next just by staying in the
vehicle. The block_id must be referenced by two or more trips in trips.txt.

- shape_id (optional)
The shape_id field contains an ID that defines a shape for the trip. This value
is referenced from the shapes.txt file. The shapes.txt file allows you to
define how a line should be drawn on the map to represent a trip.
"""

from csv import DictReader

from django.db import models

from multigtfs.models.block import Block
from multigtfs.models.route import Route
from multigtfs.models.service import Service
from multigtfs.models.shape import Shape


class Trip(models.Model):
    """A trip along a route"""

    route = models.ForeignKey(Route)
    services = models.ManyToManyField(Service)
    trip_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for a trip.")
    headsign = models.CharField(
        max_length=255, blank=True,
        help_text="Destination identification for passengers.")
    short_name = models.CharField(
        max_length=10,
        help_text="Short name used in schedules and signboards.")
    direction = models.CharField(
        max_length=1, blank=True,
        choices=(('0', 'Outbound'), ('1', 'Inbound')),
        help_text="Direction for bi-directional routes.")
    block = models.ForeignKey(
        Block, null=True,
        help_text="Block of sequential trips that this trip belongs to.")
    shape = models.ForeignKey(Shape, null=True)

    def __unicode__(self):
        return u"%s-%s" % (self.route, self.trip_id)

    class Meta:
        db_table = 'trip'
        app_label = 'multigtfs'


def import_trips_txt(trips_file, feed):
    """Import trips.txt into Trip records for feed

    Keyword arguments:
    trips_file -- A open trips.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(trips_file)
    name_map = dict(trip_headsign='headsign', trip_short_name='short_name',
                    direction_id='direction')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k, v in row.items())
        route_id = fields.pop('route_id')
        route = Route.objects.get(feed=feed, route_id=route_id)
        service_id = fields.pop('service_id')
        service = Service.objects.get(feed=feed, service_id=service_id)
        block_id = fields.pop('block_id', None)
        if block_id:
            block, _c = Block.objects.get_or_create(
                feed=feed, block_id=block_id)
        else:
            block = None
        shape_id = fields.pop('shape_id', None)
        if shape_id:
            shape = Shape.objects.get(feed=feed, shape_id=shape_id)
        else:
            shape = None
        trip_id = fields.pop('trip_id')
        trip, created = Trip.objects.get_or_create(
            trip_id=trip_id, route=route)
        for k, v in fields.items():
            if created:
                setattr(trip, k, v)
            else:
                assert getattr(trip, k) == v
        if created:
            trip.block = block
            trip.shape = shape
            trip.save()
        else:
            assert trip.block == block
            assert trip.shape == shape
        trip.services.add(service)
