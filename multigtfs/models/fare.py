"""
Define Fare model for rows in fare_attributes.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

fare_attributes.txt is optional

- fare_id (required)
The fare_id field contains an ID that uniquely identifies a fare class. The
fare_id is dataset unique.

- price (required)
The price field contains the fare price, in the unit specified by
currency_type.

- currency_type (required)
The currency_type field defines the currency used to pay the fare. Please use
the ISO 4217 alphabetical currency codes which can be found at the following
URL:

  http://www.iso.org/iso/en/prods-services/popstds/currencycodeslist.html.

- payment_method (required)
The payment_method field indicates when the fare must be paid. Valid values for
this field are:

  * 0 - Fare is paid on board.
  * 1 - Fare must be paid before boarding.

- transfers (required)
The transfers field specifies the number of transfers permitted on this fare.
Valid values for this field are:

  * 0 - No transfers permitted on this fare.
  * 1 - Passenger may transfer once.
  * 2 - Passenger may transfer twice.
  * (empty) - If this field is empty, unlimited transfers are permitted.

- transfer_duration (optional)
The transfer_duration field specifies the length of time in seconds before a
transfer expires.

When used with a transfers value of 0, the transfer_duration field indicates
how long a ticket is valid for a fare where no transfers are allowed. Unless
you intend to use this field to indicate ticket validity, transfer_duration
should be omitted or empty when transfers is set to 0.
"""

from csv import DictReader

from django.db import models

from multigtfs.utils import create_csv


class Fare(models.Model):
    """A fare class"""

    feed = models.ForeignKey('Feed')
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
        default=1,
        choices=((0, 'No transfers permitted on this fare.'),
                 (1, 'Passenger may transfer once.'),
                 (2, 'Passenger may transfer twice.'),
                 (-1, 'Unlimited transfers are permitted.')),
        help_text="Are transfers permitted?")
    transfer_duration = models.IntegerField(
        null=True,
        help_text="Time in seconds until a ticket or transfer expires")

    def __unicode__(self):
        return u"%d-%s(%s %s)" % (
            self.feed.id, self.fare_id, self.price, self.currency_type)

    class Meta:
        db_table = 'fare'
        app_label = 'multigtfs'


def import_fare_attributes_txt(fare_attributes_file, feed):
    """Import fare_attributes.txt into Fare records for feed

    Keyword arguments:
    fare_attributes_file -- A open fare_attributes.txt for reading
    feed -- the Feed to associate the records with
    """
    reader = DictReader(fare_attributes_file)
    for row in reader:
        transfer_duration = row.get('transfer_duration', None)
        row['transfer_duration'] = transfer_duration or None
        Fare.objects.create(feed=feed, **row)


def export_fare_attributes_txt(feed):
    """Export Fare records for feed into fare_attributes.txt format

    Keyword arguments:
    feed -- the Feed with the Fare records
    """
    fares = feed.fare_set
    if not fares.exists():
        return
    csv_names = [
        ('fare_id', 'fare_id'),
        ('price', 'price'),
        ('currency_type', 'currency_type'),
        ('payment_method', 'payment_method'),
        ('transfers', 'transfers')]
    if fares.exclude(transfer_duration=None).exists():
        csv_names.append(('transfer_duration', 'transfer_duration'))
    return create_csv(fares.order_by('fare_id'), csv_names)
