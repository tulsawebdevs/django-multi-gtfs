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
Define FeedInfo model for rows in feed_info.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

feed_info.txt is optional.

The file contains information about the feed itself, rather than the services
that the feed describes. GTFS currently has an agency.txt file to provide
information about the agencies that operate the services described by the feed.
However, the publisher of the feed is sometimes a different entity than any of
the agencies (in the case of regional aggregators). In addition, there are some
fields that are really feed-wide settings, rather than agency-wide.

- feed_publisher_name (required)
The feed_publisher_name field contains the full name of the organization that
publishes the feed. (This may be the same as one of the agency_name values in
agency.txt.) GTFS-consuming applications can display this name when giving
attribution for a particular feed's data.

- feed_publisher_url (required)
The feed_publisher_url field contains the URL of the feed publishing
organization's website. (This may be the same as one of the agency_url values
in agency.txt.) The value must be a fully qualified URL that includes http://
or https://, and any special characters in the URL must be correctly escaped.
See:
  http://www.w3.org/Addressing/URL/4_URI_Recommentations.html
for a description of how to create fully qualified URL values.

- feed_lang (required)
The feed_lang field contains a IETF BCP 47 language code specifying the default
language used for the text in this feed. This setting helps GTFS consumers
choose capitalization rules and other language-specific settings for the feed.
For an introduction to IETF BCP 47, please refer to:
  http://www.rfc-editor.org/rfc/bcp/bcp47.txt
  http://www.w3.org/International/articles/language-tags/
* DEV NOTE * - some historical feeds omit this parameter

- feed_start_date (optional)
- feed_end_date (optional)
The feed provides complete and reliable schedule information for service in the
period from the beginning of the feed_start_date day to the end of the
feed_end_date day. Both days are given as dates in YYYYDDMM format as for
calendar.txt, or left empty if unavailable. The feed_end_date date must not
precede the feed_start_date date if both are given. Feed providers are
encouraged to give schedule data outside this period to advise of likely future
service, but feed consumers should treat it mindful of its non-authoritative
status. If feed_start_date or feed_end_date extend beyond the active calendar
dates defined in calendar.txt and calendar_dates.txt, the feed is making an
explicit assertion that there is no service for dates within the
feed_start_date or feed_end_date range but not included in the active calendar
dates.

- feed_version (optional)
The feed publisher can specify a string here that indicates the current version
of their GTFS feed. GTFS-consuming applications can display this value to help
feed publishers determine whether the latest version of their feed has been
incorporated.
"""
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from multigtfs.models.base import models, Base


@python_2_unicode_compatible
class FeedInfo(Base):
    """Information about the feed"""
    feed = models.ForeignKey('Feed')
    publisher_name = models.CharField(
        max_length=255,
        help_text="Full name of organization that publishes the feed.")
    publisher_url = models.URLField(
        help_text="URL of the feed publisher's organization.")
    lang = models.CharField(
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
