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

from django.test import TestCase

from multigtfs.models import Feed, Zone


class ZoneTest(TestCase):
    def test_string(self):
        feed = Feed.objects.create()
        zone = Zone.objects.create(feed=feed, zone_id='ZONE')
        self.assertEqual(str(zone), '%d-ZONE' % feed.id)
