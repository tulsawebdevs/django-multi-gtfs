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
class Fare(Base):
    """A fare class"""

    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    fare_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for a fare class")
    price = models.DecimalField(
        max_digits=17, decimal_places=4,
        help_text="Fare price, in units specified by currency_type")
    currency_type = models.CharField(
        max_length=3,
        help_text="ISO 4217 alphabetical currency code")
    payment_method = models.IntegerField(
        default=1,
        choices=((0, 'Fare is paid on board.'),
                 (1, 'Fare must be paid before boarding.')),
        help_text="When is the fare paid?")
    transfers = models.IntegerField(
        default=None, null=True, blank=True,
        choices=((0, 'No transfers permitted on this fare.'),
                 (1, 'Passenger may transfer once.'),
                 (2, 'Passenger may transfer twice.'),
                 (None, 'Unlimited transfers are permitted.')),
        help_text="Are transfers permitted?")
    transfer_duration = models.IntegerField(
        null=True, blank=True,
        help_text="Time in seconds until a ticket or transfer expires")
    extra_data = JSONField(default={}, blank=True,  null=True)

    def __str__(self):
        return u"%d-%s(%s %s)" % (
            self.feed.id, self.fare_id, self.price, self.currency_type)

    class Meta:
        db_table = 'fare'
        app_label = 'multigtfs'

    # For Base import/export
    _column_map = (
        ('fare_id', 'fare_id'),
        ('price', 'price'),
        ('currency_type', 'currency_type'),
        ('payment_method', 'payment_method'),
        ('transfers', 'transfers'),
        ('transfer_duration', 'transfer_duration')
    )
    _filename = 'fare_attributes.txt'
    _unique_fields = ('fare_id',)
