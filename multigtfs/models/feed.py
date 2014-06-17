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
from zipfile import ZipFile

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import PY3

from .agency import Agency
from .fare import Fare
from .fare_rule import FareRule
from .feed_info import FeedInfo
from .frequency import Frequency
from .route import Route
from .service import Service
from .service_date import ServiceDate
from .shape import ShapePoint, post_save_shapepoint
from .stop import Stop, post_save_stop
from .stop_time import StopTime
from .transfer import Transfer
from .trip import Trip


@python_2_unicode_compatible
class Feed(models.Model):
    """Represents a single GTFS feed.

    This data is not part of the General Transit Feed Specification.  It is
    used to allow storage of several GTFS feeds in the same database.
    """
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feed'
        app_label = 'multigtfs'

    def __str__(self):
        if self.name:
            return "%d %s" % (self.id, self.name)
        else:
            return "%d" % self.id

    def import_gtfs(self, gtfs_file):
        """Import a GTFS file as feed

        Keyword arguments:
        gtfs_file - A path or file-like object for the GTFS feed

        Returns is a list of objects imported
        """
        z = ZipFile(gtfs_file, 'r')
        files = z.namelist()

        gtfs_order = (
            Agency, Stop, Route, Service, ServiceDate, ShapePoint, Trip,
            StopTime, Frequency, Fare, FareRule, Transfer, FeedInfo,
        )
        post_save.disconnect(dispatch_uid='post_save_shapepoint')
        post_save.disconnect(dispatch_uid='post_save_stop')
        try:
            for klass in gtfs_order:
                for f in files:
                    if f.endswith(klass._filename):
                        table = z.open(f)
                        if PY3:  # pragma: no cover
                            from io import TextIOWrapper
                            table = TextIOWrapper(table)
                        klass.import_txt(table, self)
        finally:
            post_save.connect(post_save_shapepoint, sender=ShapePoint)
            post_save.connect(post_save_stop, sender=Stop)

        # Update geometries
        for shape in self.shape_set.all():
            shape.update_geometry(update_parent=False)
        for trip in Trip.objects.in_feed(self):
            trip.update_geometry(update_parent=False)
        for route in self.route_set.all():
            route.update_geometry()

    def export_gtfs(self, gtfs_file):
        """Export a GTFS file as feed

        Keyword arguments:
        gtfs_file - A path or file-like object for the GTFS feed

        This function will close the file in order to finalize it.
        """
        z = ZipFile(gtfs_file, 'w')

        gtfs_order = (
            Agency, Service, ServiceDate, Fare, FareRule, FeedInfo, Frequency,
            Route, ShapePoint, StopTime, Stop, Transfer, Trip,
        )

        for exporter in gtfs_order:
            content = exporter.objects.in_feed(self).export_txt()
            if content:
                z.writestr(exporter._filename, content)
        z.close()
