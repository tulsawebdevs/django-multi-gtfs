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
import logging
import os
import os.path
import time

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import string_types
from jsonfield import JSONField

from multigtfs.compat import open_writable_zipfile, opener_from_zipfile
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

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Feed(models.Model):
    """Represents a single GTFS feed.

    This data is not part of the General Transit Feed Specification.  It is
    used to allow storage of several GTFS feeds in the same database.
    """
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    meta = JSONField(default={}, blank=True, null=True)

    class Meta:
        db_table = 'feed'
        app_label = 'multigtfs'

    def __str__(self):
        if self.name:
            return "%d %s" % (self.id, self.name)
        else:
            return "%d" % self.id

    def import_gtfs(self, gtfs_obj):
        """Import a GTFS file as feed

        Keyword arguments:
        gtfs_obj - A path to a zipped GTFS file, a path to an extracted
            GTFS file, or an open GTFS zip file.

        Returns is a list of objects imported
        """
        total_start = time.time()

        # Determine the type of gtfs_obj
        opener = None
        filelist = None
        if isinstance(gtfs_obj, string_types) and os.path.isdir(gtfs_obj):
            opener = open
            filelist = []
            for dirpath, dirnames, filenames in os.walk(gtfs_obj):
                filelist.extend([os.path.join(dirpath, f) for f in filenames])
        else:
            zfile = ZipFile(gtfs_obj, 'r')
            opener = opener_from_zipfile(zfile)
            filelist = zfile.namelist()

        gtfs_order = (
            Agency, Stop, Route, Service, ServiceDate, ShapePoint, Trip,
            StopTime, Frequency, Fare, FareRule, Transfer, FeedInfo,
        )
        post_save.disconnect(dispatch_uid='post_save_shapepoint')
        post_save.disconnect(dispatch_uid='post_save_stop')
        try:
            for klass in gtfs_order:
                for f in filelist:
                    if f.endswith(klass._filename):
                        start_time = time.time()
                        table = opener(f)
                        count = klass.import_txt(table, self) or 0
                        end_time = time.time()
                        logger.info(
                            'Imported %s (%d %s) in %0.1f seconds',
                            klass._filename, count,
                            klass._meta.verbose_name_plural,
                            end_time - start_time)
                        table.close()

        finally:
            post_save.connect(post_save_shapepoint, sender=ShapePoint)
            post_save.connect(post_save_stop, sender=Stop)

        # Update geometries
        start_time = time.time()
        for shape in self.shape_set.all():
            shape.update_geometry(update_parent=False)
        end_time = time.time()
        logger.info(
            "Updated geometries for %d shapes in %0.1f seconds",
            self.shape_set.count(), end_time - start_time)

        start_time = time.time()
        trips = Trip.objects.in_feed(self)
        for trip in trips:
            trip.update_geometry(update_parent=False)
        end_time = time.time()
        logger.info(
            "Updated geometries for %d trips in %0.1f seconds",
            trips.count(), end_time - start_time)

        start_time = time.time()
        routes = self.route_set.all()
        for route in routes:
            route.update_geometry()
        end_time = time.time()
        logger.info(
            "Updated geometries for %d routes in %0.1f seconds",
            routes.count(), end_time - start_time)

        total_end = time.time()
        logger.info(
            "Import completed in %0.1f seconds.", total_end - total_start)

    def export_gtfs(self, gtfs_file):
        """Export a GTFS file as feed

        Keyword arguments:
        gtfs_file - A path or file-like object for the GTFS feed

        This function will close the file in order to finalize it.
        """
        total_start = time.time()
        z = open_writable_zipfile(gtfs_file)

        gtfs_order = (
            Agency, Service, ServiceDate, Fare, FareRule, FeedInfo, Frequency,
            Route, ShapePoint, StopTime, Stop, Transfer, Trip,
        )

        for klass in gtfs_order:
            start_time = time.time()
            content = klass.export_txt(self)
            if content:
                z.writestr(klass._filename, content)
                end_time = time.time()
                record_count = content.count(type(content)('\n')) - 1
                logger.info(
                    'Exported %s (%d %s) in %0.1f seconds',
                    klass._filename, record_count,
                    klass._meta.verbose_name_plural,
                    end_time - start_time)
        z.close()
        total_end = time.time()
        logger.info(
            'Export completed in %0.1f seconds.', total_end - total_start)
