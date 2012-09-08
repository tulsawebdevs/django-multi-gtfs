from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand

from multigtfs.models.feed import Feed


class Command(BaseCommand):
    args = '<gtfsfeed.zip>'
    help = 'Imports a GTFS Feed from a zipped feed file'
    option_list = BaseCommand.option_list + (
        make_option(
            '-n', '--name', type='string', dest='name',
            help='Set the name of the imported feed'),)

    def handle(self, *args, **options):
        gtfs_feed = args
        name = options.get('name') or 'Imported at %s' % datetime.now()
        feed = Feed.objects.create(name=name)
        feed.import_gtfs(gtfs_feed)
        self.stdout.write("Successfully imported Feed %s" % (feed))
