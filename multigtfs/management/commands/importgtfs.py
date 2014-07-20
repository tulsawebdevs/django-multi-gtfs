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
from datetime import datetime
from optparse import make_option
import logging

from django.db import connection
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from multigtfs.models import Agency, Feed, Service


class Command(BaseCommand):
    args = '<gtfsfeed.zip>'
    help = 'Imports a GTFS Feed from a zipped feed file'
    option_list = BaseCommand.option_list + (
        make_option(
            '-n', '--name', type='string', dest='name',
            help=(
                'Set the name of the imported feed.  Defaults to name derived'
                ' from agency name and start date')),)

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must pass in the path to the feed.')
        if len(args) > 1:
            raise CommandError('You can only import one feed at a time.')
        gtfs_feed = args[0]
        unset_name = 'Imported at %s' % datetime.now()
        name = options.get('name') or unset_name

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

        feed = Feed.objects.create(name=name)
        feed.import_gtfs(gtfs_feed)

        # Set name based on feed
        if feed.name == unset_name:
            try:
                agency = feed.agency_set.order_by('id')[:1].get()
            except Agency.DoesNotExist:
                agency = None
            try:
                service = feed.service_set.order_by('id')[:1].get()
            except Service.DoesNotExist:
                service = None

            if agency:
                name = agency.name
                if service:
                    name += service.start_date.strftime(' starting %Y-%m-%d')
                else:
                    name += ' i' + unset_name[1:]
                feed.name = name
                feed.save()

        self.stdout.write("Successfully imported Feed %s\n" % (feed))
