from django.db import models


class Block(models.Model):
    """Represents a fare zone.

    This data is not represented as a file in the GTFS.  It appears as an
    identifier in the trip table.
    """
    feed = models.ForeignKey('Feed')
    block_id = models.CharField(
        max_length=10, db_index=True,
        help_text="Unique identifier for a block.")

    class Meta:
        db_table = 'block'
        app_label = 'multigtfs'
