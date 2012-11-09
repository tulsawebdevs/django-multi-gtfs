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

from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from multigtfs.models.feed import Feed


class Command(BaseCommand):
    args = '<gtfsfeed.zip>'
    help = 'Imports a GTFS Feed from a zipped feed file'
    option_list = BaseCommand.option_list + (
        make_option(
            '-n', '--name', type='string', dest='name',
            help='Set the name of the imported feed'),)

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must pass in the path to the feed.')
        if len(args) > 1:
            raise CommandError('You can only import one feed at a time.')
        gtfs_feed = args[0]
        name = options.get('name') or 'Imported at %s' % datetime.now()
        feed = Feed.objects.create(name=name)
        feed.import_gtfs(gtfs_feed)
        self.stdout.write("Successfully imported Feed %s\n" % (feed))
