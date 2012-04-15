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

from csv import DictReader

from django.db import models

from multigtfs.models.stop import Stop


class Transfer(models.Model):
    """Create additional rules for transfers between ambiguous stops"""
    from_stop = models.ForeignKey(
        Stop,
        related_name='transfer_from_stop',
        help_text='Stop where a connection between routes begins.')
    to_stop = models.ForeignKey(
        Stop,
        related_name='transfer_to_stop',
        help_text='Stop where a connection between routes ends.')
    transfer_type =  models.IntegerField(
        default=0,
        choices=((0, 'Recommended transfer point'),
                 (1, 'Timed transfer point (vehicle will wait)'),
                 (2, 'min_transfer_time needed to successfully transfer'),
                 (3, 'No transfers possible')),
        help_text="What kind of transfer?")
    min_transfer_time = models.IntegerField(
        null=True,
        help_text="How many seconds are required to transfer?")

    def __unicode__(self):
        return u"%s-%s" % (self.from_stop, self.to_stop.stop_id)

    class Meta:
        db_table = 'transfer'
        app_label = 'multigtfs'


def import_transfers_txt(transfers_file, feed):
    """Import transfers.txt into Transfer records for feed
    
    Keyword arguments:
    transfers_file -- A open transfers.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(transfers_file)
    for row in reader:
        from_stop_id = row.pop('from_stop_id')
        from_stop = Stop.objects.get(feed=feed, stop_id=from_stop_id)
        to_stop_id = row.pop('to_stop_id')
        to_stop = Stop.objects.get(feed=feed, stop_id=to_stop_id)
        # Force empty strings to 0, None
        transfer_type = row.pop('transfer_type', None)
        row['transfer_type'] = transfer_type or 0
        min_transfer_time = row.pop('min_transfer_time', None)
        row['min_transfer_time'] = min_transfer_time or None
        Transfer.objects.create(from_stop=from_stop, to_stop=to_stop, **row)
