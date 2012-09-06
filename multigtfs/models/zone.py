from django.db import models


class Zone(models.Model):
    """Represents a fare zone.

    This data is not represented as a file in the GTFS.  It appears as an
    identifier in the fare_rules and the stop tables.
    """
    feed = models.ForeignKey('Feed')
    zone_id = models.CharField(
        max_length=10, db_index=True,
        help_text="Unique identifier for a zone.")

    class Meta:
        db_table = 'zone'
        app_label = 'multigtfs'

    _rel_to_feed = 'feed'  # TODO: Delete when I'm based on GTFSModel
