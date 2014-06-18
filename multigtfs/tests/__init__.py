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

__all__ = (
    'agency', 'block', 'fare', 'fare_rule', 'feed', 'feed_info', 'fields',
    'frequency', 'route', 'service', 'service_date', 'shape', 'stop',
    'stop_time', 'transfer', 'trip', 'utils')

from multigtfs.tests.agency import AgencyTest
from multigtfs.tests.block import BlockTest
from multigtfs.tests.fare import FareTest
from multigtfs.tests.fare_rule import FareRuleTest
from multigtfs.tests.feed import FeedTest
from multigtfs.tests.feed_info import FeedInfoTest
from multigtfs.tests.fields import SecondsTest, SecondsFieldTest
from multigtfs.tests.frequency import FrequencyTest
from multigtfs.tests.route import RouteTest
from multigtfs.tests.service import ServiceTest
from multigtfs.tests.service_date import ServiceDateTest
from multigtfs.tests.shape import ShapeTest
from multigtfs.tests.stop import StopTest
from multigtfs.tests.stop_time import StopTimeTest
from multigtfs.tests.transfer import TransferTest
from multigtfs.tests.trip import TripTest
from multigtfs.tests.zone import ZoneTest

# Be quiet pyflakes
__tests = (
    AgencyTest, BlockTest, FareTest, FareRuleTest, FeedTest, FeedInfoTest,
    FrequencyTest, RouteTest, ServiceTest, ServiceDateTest, ShapeTest,
    ServiceDateTest, ShapeTest, StopTest, StopTimeTest, TransferTest,
    TripTest, SecondsTest, SecondsFieldTest, ZoneTest)
