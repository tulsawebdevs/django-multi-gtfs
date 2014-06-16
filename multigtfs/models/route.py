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
Define Route model for rows in routes.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

routes.txt is required

- route_id (required)
The route_id field contains an ID that uniquely identifies a route. The
route_id is dataset unique.

- agency_id (optional)
The agency_id field defines an agency for the specified route. This value is
referenced from the agency.txt file. Use this field when you are providing data
for routes from more than one agency.

- route_short_name (required)
The route_short_name contains the short name of a route. This will often be a
short, abstract identifier like "32", "100X", or "Green" that riders use to
identify a route, but which doesn't give any indication of what places the
route serves. If the route does not have a short name, please specify a
route_long_name and use an empty string as the value for this field.

See a Google Maps screenshot highlighting the route_short_name:
  http://bit.ly/yIS1sa

- route_long_name (required)
The route_long_name contains the full name of a route. This name is generally
more descriptive than the route_short_name and will often include the route's
destination or stop. If the route does not have a long name, please specify a
route_short_name and use an empty string as the value for this field.

See a Google Maps screenshot highlighting the route_long_name:
  http://bit.ly/wZw5yH

- route_desc (optional)
The route_desc field contains a description of a route. Please provide useful,
quality information. Do not simply duplicate the name of the route. For
example, "A trains operate between Inwood-207 St, Manhattan and Far
Rockaway-Mott Avenue, Queens at all times. Also from about 6AM until about
midnight, additional A trains operate between Inwood-207 St and Lefferts
Boulevard (trains typically alternate between Lefferts Blvd and Far Rockaway)."

- route_type (required)
The route_type field describes the type of transportation used on a route.
Valid values for this field are:

    0 - Tram, Streetcar, Light rail. Any light rail or street level system
        within a metropolitan area.
    1 - Subway, Metro. Any underground rail system within a metropolitan area.
    2 - Rail. Used for intercity or long-distance travel.
    3 - Bus. Used for short- and long-distance bus routes.
    4 - Ferry. Used for short- and long-distance boat service.
    5 - Cable car. Used for street-level cable cars where the cable runs
        beneath the car.
    6 - Gondola, Suspended cable car. Typically used for aerial cable cars
        where the car is suspended from the cable.
    7 - Funicular. Any rail system designed for steep inclines.

See a Google Maps screenshot highlighting the route_type:
  http://bit.ly/wSt2h0

- route_url (optional)
The route_url field contains the URL of a web page about that particular route.
This should be different from the agency_url.

The value must be a fully qualified URL that includes http:// or https://, and
any special characters in the URL must be correctly escaped. See
  http://www.w3.org/Addressing/URL/4_URI_Recommentations.html
for a description of how to create fully qualified URL values.

- route_color (optional)
In systems that have colors assigned to routes, the route_color field defines a
color that corresponds to a route. The color must be provided as a
six-character hexadecimal number, for example, 00FFFF. If no color is
specified, the default route color is white (FFFFFF).

The color difference between route_color and route_text_color should provide
sufficient contrast when viewed on a black and white screen. The W3C Techniques
for Accessibility Evaluation And Repair Tools document offers a useful
algorithm for evaluating color contrast:
  http://www.w3.org/TR/AERT#color-contrast

There are also helpful online tools for choosing contrasting colors, including
the snook.ca Color Contrast Check application:
  http://snook.ca/technical/colour_contrast/colour.html

- route_text_color (optional)
The route_text_color field can be used to specify a legible color to use for
text drawn against a background of route_color. The color must be provided as a
six-character hexadecimal number, for example, FFD700. If no color is
specified, the default text color is black (000000).

The color difference between route_color and route_text_color should provide
sufficient contrast when viewed on a black and white screen.
"""
from __future__ import unicode_literals

from django.contrib.gis.geos import MultiLineString
from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Route(Base):
    """A transit route"""

    feed = models.ForeignKey('Feed')
    route_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for route.")
    agency = models.ForeignKey(
        'Agency', null=True, blank=True, help_text="Agency for this route.")
    short_name = models.CharField(
        max_length=63,
        help_text="Short name of the route")
    long_name = models.CharField(
        max_length=255,
        help_text="Long name of the route")
    desc = models.TextField(
        blank=True,
        help_text="Long description of a route")
    rtype = models.IntegerField(
        choices=((0, 'Tram, Streetcar, or Light rail'),
                 (1, 'Subway or Metro'),
                 (2, 'Rail'),
                 (3, 'Bus'),
                 (4, 'Ferry'),
                 (5, 'Cable car'),
                 (6, 'Gondola or Suspended cable car'),
                 (7, 'Funicular')),
        help_text='Type of transportation used on route')
    url = models.URLField(
        blank=True, help_text="Web page about for the route")
    color = models.CharField(
        max_length=6, blank=True,
        help_text="Color of route in hex")
    text_color = models.CharField(
        max_length=6, blank=True,
        help_text="Color of route text in hex")
    geometry = models.MultiLineStringField(
        null=True, blank=True,
        help_text='Geometry cache of Trips')

    def update_geometry(self):
        """Update the geometry from the Trips"""
        original = self.geometry
        trips = self.trip_set.exclude(geometry=None)
        unique_coords = set()
        unique_geom = list()
        for t in trips:
            coords = t.geometry.coords
            if coords not in unique_coords:
                unique_coords.add(coords)
                unique_geom.append(t.geometry)
        self.geometry = MultiLineString(unique_geom)
        if self.geometry != original:
            self.save()

    def __str__(self):
        return "%d-%s" % (self.feed.id, self.route_id)

    class Meta:
        db_table = 'route'
        app_label = 'multigtfs'

    _column_map = (
        ('route_id', 'route_id'),
        ('agency_id', 'agency__agency_id'),
        ('route_short_name', 'short_name'),
        ('route_long_name', 'long_name'),
        ('route_desc', 'desc'),
        ('route_type', 'rtype'),
        ('route_url', 'url'),
        ('route_color', 'color'),
        ('route_text_color', 'text_color')
    )
    _filename = 'routes.txt'
    _sort_order = ('route_id', 'short_name')
    _unique_fields = ('route_id',)
