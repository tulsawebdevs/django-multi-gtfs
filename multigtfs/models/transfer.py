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

"""
Define Transfers model for rows in transfer.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

transfer.txt is optional.

Trip planners normally calculate transfer points based on the relative
proximity of stops in each route. For potentially ambiguous stop pairs, or
transfers where you want to specify a particular choice, use transfers.txt to
define additional rules for making connections between routes.

- from_stop_id (required)
The from_stop_id field contains a stop ID that identifies a stop or station
where a connection between routes begins. Stop IDs are referenced from the
stops.txt file. If the stop ID refers to a station that contains multiple
stops, this transfer rule applies to all stops in that station.

- to_stop_id (required)
The to_stop_id field contains a stop ID that identifies a stop or station where
a connection between routes ends. Stop IDs are referenced from the stops.txt
file. If the stop ID refers to a station that contains multiple stops, this
transfer rule applies to all stops in that station.

- transfer_type (required)
The transfer_type field specifies the type of connection for the specified
(from_stop_id, to_stop_id) pair. Valid values for this field are:

    0 or (empty) - This is a recommended transfer point between two routes.
    1 - This is a timed transfer point between two routes. The departing
        vehicle is expected to wait for the arriving one, with sufficient time
        for a passenger to transfer between routes.
    2 - This transfer requires a minimum amount of time between arrival and
        departure to ensure a connection. The time required to transfer is
        specified by min_transfer_time.
    3 - Transfers are not possible between routes at this location.

- min_transfer_time (optional)
When a connection between routes requires an amount of time between arrival and
departure (transfer_type=2), the min_transfer_time field defines the amount of
time that must be available in an itinerary to permit a transfer between routes
at these stops. The min_transfer_time must be sufficient to permit a typical
rider to move between the two stops, including buffer time to allow for
schedule variance on each route.

The min_transfer_time value must be entered in seconds, and must be a
non-negative integer.
"""
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Transfer(Base):
    """Create additional rules for transfers between ambiguous stops"""
    from_stop = models.ForeignKey(
        'Stop',
        related_name='transfer_from_stop',
        help_text='Stop where a connection between routes begins.')
    to_stop = models.ForeignKey(
        'Stop',
        related_name='transfer_to_stop',
        help_text='Stop where a connection between routes ends.')
    transfer_type = models.IntegerField(
        default=0, blank=True,
        choices=((0, 'Recommended transfer point'),
                 (1, 'Timed transfer point (vehicle will wait)'),
                 (2, 'min_transfer_time needed to successfully transfer'),
                 (3, 'No transfers possible')),
        help_text="What kind of transfer?")
    min_transfer_time = models.IntegerField(
        null=True, blank=True,
        help_text="How many seconds are required to transfer?")

    def __str__(self):
        return "%s-%s" % (self.from_stop, self.to_stop.stop_id)

    class Meta:
        db_table = 'transfer'
        app_label = 'multigtfs'

    _column_map = (
        ('from_stop_id', 'from_stop__stop_id'),
        ('to_stop_id', 'to_stop__stop_id'),
        ('transfer_type', 'transfer_type'),
        ('min_transfer_time', 'min_transfer_time')
    )
    _filename = 'transfers.txt'
    _rel_to_feed = 'from_stop__feed'
    _sort_order = ('from_stop__stop_id', 'to_stop__stop_id')
    _unique_fields = ('from_stop_id', 'to_stop_id')
