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
import logging

from django.db import connection
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from multigtfs.models.feed import Feed


class Command(BaseCommand):
    help = 'Exports a GTFS Feed to a zipped feed file'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('feed_id',
                            metavar='GTFS Feed ID',
                            type=int)

        # Named (optional) arguments
        parser.add_argument('-n', '--name',
                            type=str,
                            dest='name',
                            help='Set the name of the exported feed')

    def handle(self, *args, **options):
        # Setup logging
        verbosity = int(options['verbosity'])
        console = logging.StreamHandler(self.stderr)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        logger_name = 'multigtfs'
        if verbosity == 0:
            level = logging.WARNING
        elif verbosity == 1:
            level = logging.INFO
        elif verbosity == 2:
            level = logging.DEBUG
        else:
            level = logging.DEBUG
            logger_name = ''
            formatter = logging.Formatter(
                '%(name)s - %(levelname)s - %(message)s')
        console.setLevel(level)
        console.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(console)

        # Disable database query logging
        if settings.DEBUG:
            connection.use_debug_cursor = False

        feed_id = options.get('feed_id')

        try:
            feed = Feed.objects.get(id=feed_id)
        except Feed.DoesNotExist:
            raise CommandError('Feed %s not found' % feed_id)
        out_name = options.get('name') or slugify(feed.name)
        if not out_name.endswith('.zip'):
            out_name += '.zip'
        self.stdout.write(
            "Exporting Feed %s to %s...\n" % (feed_id, out_name))
        feed.export_gtfs(out_name)
        self.stdout.write(
            "Successfully exported Feed %s to %s\n" % (feed_id, out_name))
