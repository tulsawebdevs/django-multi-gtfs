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
class Agency(Base):
    """One or more transit agencies that provide the data in this feed.

    Maps to agency.txt in the GTFS feed.
    """
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    agency_id = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text="Unique identifier for transit agency")
    name = models.CharField(
        max_length=255,
        help_text="Full name of the transit agency")
    url = models.URLField(
        blank=True, help_text="URL of the transit agency")
    timezone = models.CharField(
        max_length=255,
        help_text="Timezone of the agency")
    lang = models.CharField(
        max_length=2, blank=True,
        help_text="ISO 639-1 code for the primary language")
    phone = models.CharField(
        max_length=255, blank=True,
        help_text="Voice telephone number")
    fare_url = models.URLField(
        blank=True, help_text="URL for purchasing tickets online")
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return u"%d-%s" % (self.feed.id, self.agency_id)

    class Meta:
        db_table = 'agency'
        app_label = 'multigtfs'
        verbose_name_plural = "agencies"

    # GTFS column names to fields, used by Base for import/export
    _column_map = (
        ('agency_id', 'agency_id'),
        ('agency_name', 'name'),
        ('agency_url', 'url'),
        ('agency_timezone', 'timezone'),
        ('agency_lang', 'lang'),
        ('agency_phone', 'phone'),
        ('agency_fare_url', 'fare_url')
    )
    _filename = 'agency.txt'
    _unique_fields = ('agency_id',)
