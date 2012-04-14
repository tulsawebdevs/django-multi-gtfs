from django.db import models


class Feed(models.Model):
    """Represents a single GTFS feed.

    This data is not part of the General Transit Feed Specification.  It is
    used to allow storage of several GTFS feeds in the same database.
    """
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        if self.name:
            return u"%d %s" % (self.id, self.name)
        else:
            return u"%d" % self.id

    class Meta:
        db_table = 'feed'
        app_label = 'multigtfs'
