#
# Copyright 2012 John Whitlock
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

from zipfile import ZipFile

from django.db import models

from agency import Agency
from fare import Fare
from fare_rule import FareRule
from feed_info import FeedInfo
from frequency import Frequency
from route import Route
from service import Service
from service_date import ServiceDate
from shape import ShapePoint
from stop import Stop
from stop_time import StopTime
from transfer import Transfer
from trip import Trip


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

    def __unicode__(self):
        if self.name:
            return u"%d %s" % (self.id, self.name)
        else:
            return u"%d" % self.id

    def import_gtfs(self, gtfs_file):
        """Import a GTFS file as feed

        Keyword arguments:
        gtfs_file - A path or file-like object for the GTFS feed

        Returns is a list of objects imported
        """
        z = ZipFile(gtfs_file, 'r')
        files = z.namelist()

        gtfs_order = (
            ('agency.txt', Agency),
            ('stops.txt', Stop),
            ('routes.txt', Route),
            ('calendar.txt', Service),
            ('calendar_dates.txt', ServiceDate),
            ('shapes.txt', ShapePoint),
            ('trips.txt', Trip),
            ('stop_times.txt', StopTime),
            ('frequencies.txt', Frequency),
            ('fare_attributes.txt', Fare),
            ('fare_rules.txt', FareRule),
            ('transfers.txt', Transfer),
            ('feed_info.txt', FeedInfo),
        )

        for table_name, klass in gtfs_order:
            for f in files:
                if f.endswith(table_name):
                    table = z.open(f)
                    klass.import_txt(table, self)

    def export_gtfs(self, gtfs_file):
        """Export a GTFS file as feed

        Keyword arguments:
        gtfs_file - A path or file-like object for the GTFS feed

        This function will close the file in order to finalize it.
        """
        z = ZipFile(gtfs_file, 'w')

        gtfs_order = (
            ('agency.txt', Agency),
            ('calendar.txt', Service),
            ('calendar_dates.txt', ServiceDate),
            ('fare_attributes.txt', Fare),
            ('fare_rules.txt', FareRule),
            ('feed_info.txt', FeedInfo),
            ('frequencies.txt', Frequency),
            ('routes.txt', Route),
            ('shapes.txt', ShapePoint),
            ('stop_times.txt', StopTime),
            ('stops.txt', Stop),
            ('transfers.txt', Transfer),
            ('trips.txt', Trip),
        )

        for filename, exporter in gtfs_order:
            content = exporter.objects.in_feed(self).export_txt()
            if content:
                z.writestr(filename, content)
        z.close()
