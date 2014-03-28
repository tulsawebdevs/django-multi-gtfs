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

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from multigtfs.models import Feed, Route, Shape, Trip


class Command(BaseCommand):
    args = '--all | <feed ID 1> <feed ID 2> ...'
    help = 'Updates the cached geometry of GTFS feeds'
    option_list = BaseCommand.option_list + (
        make_option(
            '-a', '--all', action='store_true', dest='all', default=False,
            help='update all feeds'),
        make_option(
            '-q', '--quiet', action='store_false', dest='verbose',
            default=True, help="don't print status messages to stdout"),
    )

    def handle(self, *args, **options):
        # Validate the arguments
        all_feeds = options.get('all')
        verbose = options.get('verbose')
        if len(args) == 0 and not all_feeds:
            raise CommandError('You must pass in feed ID or --all.')
        if len(args) > 0 and all_feeds:
            raise CommandError("You can't specify a feeds and --all.")

        # Get the feeds
        if all_feeds:
            feeds = Feed.objects.order_by('id')
        else:
            feeds = []
            feed_ids = [int(a) for a in args]
            for feed_id in feed_ids:
                try:
                    feeds.append(Feed.objects.get(id=feed_id))
                except Feed.DoesNotExist:
                    raise CommandError('Feed %s not found' % feed_id)

        # Refresh the geometries
        for feed in feeds:
            if verbose:
                self.stdout.write(
                    "Updating geometries in Feed %s (ID %s)...\n" % (
                        feed.name, feed.id))
            shapes = Shape.objects.in_feed(feed)
            trips = Trip.objects.in_feed(feed)
            routes = Route.objects.in_feed(feed)
            for shape in shapes:
                shape.update_geometry(update_parent=False)
            for trip in trips:
                trip.update_geometry(update_parent=False)
            for route in routes:
                route.update_geometry()

            if verbose:
                self.stdout.write(
                    "Feed %d: Updated geometries in %d shape%s, %d trip%s, and"
                    " %d route%s." % (
                        feed.id,
                        shapes.count(), '' if shapes.count() == 1 else 's',
                        trips.count(), '' if trips.count() == 1 else 's',
                        routes.count(), '' if routes.count() == 1 else 's'))
