from zipfile import ZipFile

from django.db import models

from multigtfs.models.agency import import_agency_txt, export_agency_txt
from multigtfs.models.fare import (
    import_fare_attributes_txt, export_fare_attributes_txt)
from multigtfs.models.fare_rule import (
    import_fare_rules_txt, export_fare_rules_txt)
from multigtfs.models.feed_info import import_feed_info_txt
from multigtfs.models.frequency import import_frequencies_txt
from multigtfs.models.route import import_routes_txt
from multigtfs.models.service import import_calendar_txt, export_calendar_txt
from multigtfs.models.service_date import (
    import_calendar_dates_txt, export_calendar_dates_txt)
from multigtfs.models.shape import import_shapes_txt
from multigtfs.models.stop import import_stops_txt
from multigtfs.models.stop_time import import_stop_times_txt
from multigtfs.models.transfer import import_transfers_txt
from multigtfs.models.trip import import_trips_txt


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
            ('agency.txt', import_agency_txt),
            ('stops.txt', import_stops_txt),
            ('routes.txt', import_routes_txt),
            ('calendar.txt', import_calendar_txt),
            ('calendar_dates.txt', import_calendar_dates_txt),
            ('shapes.txt', import_shapes_txt),
            ('trips.txt', import_trips_txt),
            ('stop_times.txt', import_stop_times_txt),
            ('frequencies.txt', import_frequencies_txt),
            ('fare_attributes.txt', import_fare_attributes_txt),
            ('fare_rules.txt', import_fare_rules_txt),
            ('transfers.txt', import_transfers_txt),
            ('feed_info.txt', import_feed_info_txt),
        )

        for table_name, importer in gtfs_order:
            for f in files:
                if f.endswith(table_name):
                    table = z.open(f)
                    importer(table, self)

    def export_gtfs(self, gtfs_file):
        """Export a GTFS file as feed
        
        Keyword arguments:
        gtfs_file - A path or file-like object for the GTFS feed
        
        This function will close the file in order to finalize it.
        """
        z = ZipFile(gtfs_file, 'w')

        gtfs_order = (
            ('agency.txt', export_agency_txt),
            ('calendar.txt', export_calendar_txt),
            ('calendar_dates.txt', export_calendar_dates_txt),
            ('fare_attributes.txt', export_fare_attributes_txt),
            ('fare_rules.txt', export_fare_rules_txt),
            # ('feed_info.txt', export_feed_info_txt),
            # ('frequencies.txt', export_frequencies_txt),
            # ('routes.txt', export_routes_txt),
            # ('shapes.txt', export_shapes_txt),
            # ('stop_times.txt', export_stop_times_txt),
            # ('stops.txt', export_stops_txt),
            # ('transfers.txt', export_transfers_txt),
            # ('trips.txt', export_trips_txt),
        )

        for filename, exporter in gtfs_order:
            path = 'feed/%s' % filename
            content = exporter(self)
            if content:
                z.writestr(path, content)
        z.close()
