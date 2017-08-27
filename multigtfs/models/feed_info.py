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
class FeedInfo(Base):
    """Information about the feed

    Implements feed_info.txt in the GTFS feed.
    """
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    publisher_name = models.CharField(
        max_length=255,
        help_text="Full name of organization that publishes the feed.")
    publisher_url = models.URLField(
        help_text="URL of the feed publisher's organization.")
    lang = models.CharField(
        "language",
        max_length=20,
        help_text="IETF BCP 47 language code for text in field.")
    start_date = models.DateField(
        null=True, blank=True,
        help_text="Date that feed starts providing reliable data.")
    end_date = models.DateField(
        null=True, blank=True,
        help_text="Date that feed stops providing reliable data.")
    version = models.CharField(
        max_length=255, blank=True,
        help_text="Version of feed.")
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return '%s-%s' % (self.feed.id, self.publisher_name)

    class Meta:
        db_table = 'feed_info'
        app_label = 'multigtfs'
        verbose_name_plural = "feed info"

    _column_map = (
        ('feed_publisher_name', 'publisher_name'),
        ('feed_publisher_url', 'publisher_url'),
        ('feed_lang', 'lang'),
        ('feed_start_date', 'start_date'),
        ('feed_end_date', 'end_date'),
        ('feed_version', 'version')
    )
    _filename = 'feed_info.txt'
    _unique_fields = ('feed_publisher_name',)
