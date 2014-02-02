'''Settings specific to django-multi-gtfs'''

from django.conf import settings

# PostGIS 1.5 added support for the geography type, with native support for
# spatial features represented in geographic coordinates (WGS84 long/lat).
# The main differences from the previous geometric types are that:
# 1) Geography distances use the more mathematically-intense great circle arc
#    calculations, returning linear distances
# 2) Geometric distances return distances in degrees, but is faster
# 3) Only a subset of spatial lookups are available for geographic types
#
# We default to the geometry type with SRID 4326 (WGS84).  If you know what
# you are doing, you may want to use a different SRID or even the geography
# type.
#
# See the docs:
# https://docs.djangoproject.com/en/dev/ref/contrib/gis/model-api/
#   See "Geography Type"
#   Direct link: http://goo.gl/Vh0piU
# http://postgis.refractions.net/documentation/manual-1.5/ch04.html
#   See "4.2.2. When to use Geography Data type over Geometry data type"
#   Direct link: http://goo.gl/bOMYw7

MULTIGTFS_USE_GEOGRAPHY = getattr(settings, 'MULTIGTFS_USE_GEOGRAPHY', False)
MULTIGTFS_SRID = getattr(settings, 'MULTIGTFS_SRID', 4326)

# If you fulfill the requirements, the OpenStreetMap layer is nicer
# https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#osmgeoadmin
MULTIGTFS_OSMADMIN = getattr(settings, 'MULTIGTFS_OSMADMIN', True)
