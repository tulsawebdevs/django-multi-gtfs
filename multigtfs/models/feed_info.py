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

from csv import DictReader
from datetime import datetime

from django.db import models


class FeedInfo(models.Model):
    """Information about the feed"""
    feed = models.ForeignKey('Feed')
    publisher_name = models.CharField(
        max_length=255,
        help_text="Full name of organization that publishes the feed.")
    publisher_url = models.URLField(
        verify_exists=False,
        help_text="URL of the feed publisher's organization.")
    lang = models.CharField(
        max_length=20,
        help_text="IETF BCP 47 language code for text in field.")
    start_date = models.DateField(
        null=True,
        help_text="Date that feed starts providing reliable data.")
    end_date = models.DateField(
        null=True,
        help_text="Date that feed stops providing reliable data.")
    version = models.CharField(
        max_length=20, blank=True,
        help_text="Version of feed.")

    def __unicode__(self):
        return u'%s-%s' % (self.feed.id, self.publisher_name)

    class Meta:
        db_table = 'feed_info'
        app_label = 'multigtfs'
        verbose_name_plural = "feed info"


def import_feed_info_txt(feed_info_file, feed):
    """Import feed_info.txt into a FeedInfo record for feed

    Keyword arguments:
    feed_info_file -- A open transfers.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(feed_info_file)
    name_map = dict(feed_publisher_name='publisher_name',
                    feed_publisher_url='publisher_url', feed_lang='lang',
                    feed_start_date='start_date', feed_end_date='end_date',
                    feed_version='version')
    for row in reader:
        fields = dict((name_map.get(k, k), v) for k, v in row.items())
        start_date_raw = fields.pop('start_date', None)
        if start_date_raw:
            start_date = datetime.strptime(start_date_raw, '%Y%m%d')
        else:
            start_date = None
        end_date_raw = fields.pop('end_date', None)
        if end_date_raw:
            end_date = datetime.strptime(end_date_raw, '%Y%m%d')
        else:
            end_date = None

        FeedInfo.objects.create(feed=feed, start_date=start_date,
            end_date=end_date, **fields)
