from zipfile import ZipFile

from django.db import models

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
        from multigtfs.models import (
            Agency, Fare, FareRule, FeedInfo, Frequency, Route, Service,
            ServiceDate, ShapePoint, Stop, StopTime)

        z = ZipFile(gtfs_file, 'r')
        files = z.namelist()

        gtfs_order = (
            ('agency.txt', Agency),
            ('stops.txt', Stop),
            ('routes.txt', Route),
            ('calendar.txt', Service),
            ('calendar_dates.txt', ServiceDate),
            ('shapes.txt', ShapePoint),
            ('trips.txt', import_trips_txt),
            ('stop_times.txt', StopTime),
            ('frequencies.txt', Frequency),
            ('fare_attributes.txt', Fare),
            ('fare_rules.txt', FareRule),
            ('transfers.txt', import_transfers_txt),
            ('feed_info.txt', FeedInfo),
        )

        for table_name, importer in gtfs_order:
            for f in files:
                if f.endswith(table_name):
                    table = z.open(f)
                    if hasattr(importer, 'import_txt'):
                        importer.import_txt(table, self)
                    else:
                        importer(table, self)

    def export_gtfs(self, gtfs_file):
        """Export a GTFS file as feed

        Keyword arguments:
        gtfs_file - A path or file-like object for the GTFS feed

        This function will close the file in order to finalize it.
        """
        from multigtfs.models import (
            Agency, Fare, FareRule, FeedInfo, Frequency, Route, Service,
            ServiceDate, ShapePoint, Stop, StopTime)

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
            # ('transfers.txt', export_transfers_txt),
            # ('trips.txt', export_trips_txt),
        )

        for filename, exporter in gtfs_order:
            path = 'feed/%s' % filename
            content = exporter.objects.in_feed(self).export_txt()
            if content:
                z.writestr(path, content)
        z.close()
