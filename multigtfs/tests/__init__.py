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

from multigtfs.tests.test_agency import AgencyTest
from multigtfs.tests.test_block import BlockTest
from multigtfs.tests.test_fare import FareTest
from multigtfs.tests.test_fare_rule import FareRuleTest
from multigtfs.tests.test_feed import FeedTest
from multigtfs.tests.test_feed_info import FeedInfoTest
from multigtfs.tests.test_fields import SecondsTest, SecondsFieldTest
from multigtfs.tests.test_frequency import FrequencyTest
from multigtfs.tests.test_route import RouteTest
from multigtfs.tests.test_service import ServiceTest
from multigtfs.tests.test_service_date import ServiceDateTest
from multigtfs.tests.test_shape import ShapeTest
from multigtfs.tests.test_stop import StopTest
from multigtfs.tests.test_stop_time import StopTimeTest
from multigtfs.tests.test_transfer import TransferTest
from multigtfs.tests.test_trip import TripTest
from multigtfs.tests.test_zone import ZoneTest

__all__ = (
    'agency', 'block', 'fare', 'fare_rule', 'feed', 'feed_info', 'fields',
    'frequency', 'route', 'service', 'service_date', 'shape', 'stop',
    'stop_time', 'transfer', 'trip', 'utils')


# Be quiet pyflakes
__tests = (
    AgencyTest, BlockTest, FareTest, FareRuleTest, FeedTest, FeedInfoTest,
    FrequencyTest, RouteTest, ServiceTest, ServiceDateTest, ShapeTest,
    ServiceDateTest, ShapeTest, StopTest, StopTimeTest, TransferTest,
    TripTest, SecondsTest, SecondsFieldTest, ZoneTest)
