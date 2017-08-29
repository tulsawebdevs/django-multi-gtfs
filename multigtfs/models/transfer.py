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

from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class Transfer(Base):
    """Create additional rules for transfers between ambiguous stops.

    Implements transfer.txt in the GTFS feed.
    """
    from_stop = models.ForeignKey(
        'Stop', on_delete=models.CASCADE,
        related_name='transfer_from_stop',
        help_text='Stop where a connection between routes begins.')
    to_stop = models.ForeignKey(
        'Stop', on_delete=models.CASCADE,
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
    extra_data = JSONField(default={}, blank=True, null=True)

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
