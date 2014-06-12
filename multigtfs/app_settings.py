'''Settings specific to django-multi-gtfs'''
from __future__ import unicode_literals

from django.conf import settings

# If you fulfill the requirements, the OpenStreetMap layer is nicer
# https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#osmgeoadmin
MULTIGTFS_OSMADMIN = getattr(settings, 'MULTIGTFS_OSMADMIN', True)
