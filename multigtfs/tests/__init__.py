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

# Be quiet pyflakes
__tests = (
    AgencyTest, BlockTest, FareTest, FareRuleTest, FeedTest, FeedInfoTest,
    FrequencyTest, RouteTest, ServiceTest, ServiceDateTest, ShapeTest,
    ServiceDateTest, ShapeTest, StopTest, StopTimeTest, TransferTest,
    TripTest, SecondsTest, SecondsFieldTest)
