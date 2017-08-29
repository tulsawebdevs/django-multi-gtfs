# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.contrib.gis.db.models.fields
import multigtfs.models.fields.seconds


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agency_id', models.CharField(help_text='Unique identifier for transit agency', max_length=255, db_index=True, blank=True)),
                ('name', models.CharField(help_text='Full name of the transit agency', max_length=255)),
                ('url', models.URLField(help_text='URL of the transit agency', blank=True)),
                ('timezone', models.CharField(help_text='Timezone of the agency', max_length=255)),
                ('lang', models.CharField(help_text='ISO 639-1 code for the primary language', max_length=2, blank=True)),
                ('phone', models.CharField(help_text='Voice telephone number', max_length=255, blank=True)),
                ('fare_url', models.URLField(help_text='URL for purchasing tickets online', blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
            ],
            options={
                'db_table': 'agency',
                'verbose_name_plural': 'agencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block_id', models.CharField(help_text='Unique identifier for a block.', max_length=63, db_index=True)),
            ],
            options={
                'db_table': 'block',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fare_id', models.CharField(help_text='Unique identifier for a fare class', max_length=255, db_index=True)),
                ('price', models.DecimalField(help_text='Fare price, in units specified by currency_type', max_digits=17, decimal_places=4)),
                ('currency_type', models.CharField(help_text='ISO 4217 alphabetical currency code', max_length=3)),
                ('payment_method', models.IntegerField(default=1, help_text='When is the fare paid?', choices=[(0, 'Fare is paid on board.'), (1, 'Fare must be paid before boarding.')])),
                ('transfers', models.IntegerField(default=None, help_text='Are transfers permitted?', null=True, blank=True, choices=[(0, 'No transfers permitted on this fare.'), (1, 'Passenger may transfer once.'), (2, 'Passenger may transfer twice.'), (None, 'Unlimited transfers are permitted.')])),
                ('transfer_duration', models.IntegerField(help_text='Time in seconds until a ticket or transfer expires', null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
            ],
            options={
                'db_table': 'fare',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FareRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
            ],
            options={
                'db_table': 'fare_rules',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('meta', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
            ],
            options={
                'db_table': 'feed',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publisher_name', models.CharField(help_text='Full name of organization that publishes the feed.', max_length=255)),
                ('publisher_url', models.URLField(help_text="URL of the feed publisher's organization.")),
                ('lang', models.CharField(help_text='IETF BCP 47 language code for text in field.', max_length=20, verbose_name='language')),
                ('start_date', models.DateField(help_text='Date that feed starts providing reliable data.', null=True, blank=True)),
                ('end_date', models.DateField(help_text='Date that feed stops providing reliable data.', null=True, blank=True)),
                ('version', models.CharField(help_text='Version of feed.', max_length=255, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('feed', models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'feed_info',
                'verbose_name_plural': 'feed info',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', multigtfs.models.fields.seconds.SecondsField(help_text='Time that the service begins at the specified frequency')),
                ('end_time', multigtfs.models.fields.seconds.SecondsField(help_text='Time that the service ends at the specified frequency')),
                ('headway_secs', models.IntegerField(help_text='Time in seconds before returning to same stop')),
                ('exact_times', models.CharField(blank=True, help_text='Should frequency-based trips be exactly scheduled?', max_length=1, choices=[(0, 'Trips are not exactly scheduled'), (1, 'Trips are exactly scheduled from start time')])),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
            ],
            options={
                'db_table': 'frequency',
                'verbose_name_plural': 'frequencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('route_id', models.CharField(help_text='Unique identifier for route.', max_length=255, db_index=True)),
                ('short_name', models.CharField(help_text='Short name of the route', max_length=63)),
                ('long_name', models.CharField(help_text='Long name of the route', max_length=255)),
                ('desc', models.TextField(help_text='Long description of a route', verbose_name='description', blank=True)),
                ('rtype', models.IntegerField(help_text='Type of transportation used on route', verbose_name='route type', choices=[(0, 'Tram, Streetcar, or Light rail'), (1, 'Subway or Metro'), (2, 'Rail'), (3, 'Bus'), (4, 'Ferry'), (5, 'Cable car'), (6, 'Gondola or Suspended cable car'), (7, 'Funicular')])),
                ('url', models.URLField(help_text='Web page about for the route', blank=True)),
                ('color', models.CharField(help_text='Color of route in hex', max_length=6, blank=True)),
                ('text_color', models.CharField(help_text='Color of route text in hex', max_length=6, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiLineStringField(help_text='Geometry cache of Trips', srid=4326, null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('agency', models.ForeignKey(blank=True, to='multigtfs.Agency', help_text='Agency for this route.', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('feed', models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'route',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_id', models.CharField(help_text='Unique identifier for service dates.', max_length=255, db_index=True)),
                ('monday', models.BooleanField(default=True, help_text='Is the route active on Monday?')),
                ('tuesday', models.BooleanField(default=True, help_text='Is the route active on Tuesday?')),
                ('wednesday', models.BooleanField(default=True, help_text='Is the route active on Wednesday?')),
                ('thursday', models.BooleanField(default=True, help_text='Is the route active on Thursday?')),
                ('friday', models.BooleanField(default=True, help_text='Is the route active on Friday?')),
                ('saturday', models.BooleanField(default=True, help_text='Is the route active on Saturday?')),
                ('sunday', models.BooleanField(default=True, help_text='Is the route active on Sunday?')),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('feed', models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'service',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(help_text='Date that the service differs from the norm.')),
                ('exception_type', models.IntegerField(default=1, help_text='Is service added or removed on this date?', choices=[(1, 'Added'), (2, 'Removed')])),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('service', models.ForeignKey(to='multigtfs.Service', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'service_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shape_id', models.CharField(help_text='Unique identifier for a shape.', max_length=255, db_index=True)),
                ('geometry', django.contrib.gis.db.models.fields.LineStringField(help_text='Geometry cache of ShapePoints', srid=4326, null=True, blank=True)),
                ('feed', models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'shape',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShapePoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text='WGS 84 latitude/longitude of shape point', srid=4326)),
                ('sequence', models.IntegerField()),
                ('traveled', models.FloatField(help_text='Distance of point from start of shape', null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('shape', models.ForeignKey(related_name='points', to='multigtfs.Shape', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'shape_point',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stop_id', models.CharField(help_text='Unique identifier for a stop or station.', max_length=255, db_index=True)),
                ('code', models.CharField(help_text='Uniquer identifier (short text or number) for passengers.', max_length=255, blank=True)),
                ('name', models.CharField(help_text='Name of stop in local vernacular.', max_length=255)),
                ('desc', models.CharField(help_text='Description of a stop.', max_length=255, verbose_name='description', blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text='WGS 84 latitude/longitude of stop or station', srid=4326)),
                ('url', models.URLField(help_text='URL for the stop', blank=True)),
                ('location_type', models.CharField(blank=True, help_text='Is this a stop or station?', max_length=1, choices=[('0', 'Stop'), ('1', 'Station')])),
                ('timezone', models.CharField(help_text='Timezone of the stop', max_length=255, blank=True)),
                ('wheelchair_boarding', models.CharField(blank=True, help_text='Is wheelchair boarding possible?', max_length=1, choices=[('0', 'No information'), ('1', 'Some wheelchair boarding'), ('2', 'No wheelchair boarding')])),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('feed', models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE)),
                ('parent_station', models.ForeignKey(blank=True, to='multigtfs.Stop', help_text='The station associated with the stop', null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'stop',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StopTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arrival_time', multigtfs.models.fields.seconds.SecondsField(default=None, help_text='Arrival time. Must be set for end stops of trip.', null=True, blank=True)),
                ('departure_time', multigtfs.models.fields.seconds.SecondsField(default=None, help_text='Departure time. Must be set for end stops of trip.', null=True, blank=True)),
                ('stop_sequence', models.IntegerField()),
                ('stop_headsign', models.CharField(help_text='Sign text that identifies the stop for passengers', max_length=255, blank=True)),
                ('pickup_type', models.CharField(blank=True, help_text='How passengers are picked up', max_length=1, choices=[('0', 'Regularly scheduled pickup'), ('1', 'No pickup available'), ('2', 'Must phone agency to arrange pickup'), ('3', 'Must coordinate with driver to arrange pickup')])),
                ('drop_off_type', models.CharField(blank=True, help_text='How passengers are picked up', max_length=1, choices=[('0', 'Regularly scheduled drop off'), ('1', 'No drop off available'), ('2', 'Must phone agency to arrange drop off'), ('3', 'Must coordinate with driver to arrange drop off')])),
                ('shape_dist_traveled', models.FloatField(help_text='Distance of stop from start of shape', null=True, verbose_name='shape distance traveled', blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('stop', models.ForeignKey(to='multigtfs.Stop', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'stop_time',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transfer_type', models.IntegerField(default=0, help_text='What kind of transfer?', blank=True, choices=[(0, 'Recommended transfer point'), (1, 'Timed transfer point (vehicle will wait)'), (2, 'min_transfer_time needed to successfully transfer'), (3, 'No transfers possible')])),
                ('min_transfer_time', models.IntegerField(help_text='How many seconds are required to transfer?', null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('from_stop', models.ForeignKey(related_name='transfer_from_stop', to='multigtfs.Stop', help_text='Stop where a connection between routes begins.', on_delete=django.db.models.deletion.CASCADE)),
                ('to_stop', models.ForeignKey(related_name='transfer_to_stop', to='multigtfs.Stop', help_text='Stop where a connection between routes ends.', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'transfer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trip_id', models.CharField(help_text='Unique identifier for a trip.', max_length=255, db_index=True)),
                ('headsign', models.CharField(help_text='Destination identification for passengers.', max_length=255, blank=True)),
                ('short_name', models.CharField(help_text='Short name used in schedules and signboards.', max_length=63, blank=True)),
                ('direction', models.CharField(blank=True, help_text='Direction for bi-directional routes.', max_length=1, choices=[('0', '0'), ('1', '1')])),
                ('geometry', django.contrib.gis.db.models.fields.LineStringField(help_text='Geometry cache of Shape or Stops', srid=4326, null=True, blank=True)),
                ('wheelchair_accessible', models.CharField(blank=True, help_text='Are there accommodations for riders with wheelchair?', max_length=1, choices=[('0', 'No information'), ('1', 'Some wheelchair accommodation'), ('2', 'No wheelchair accommodation')])),
                ('bikes_allowed', models.CharField(blank=True, help_text='Are bicycles allowed?', max_length=1, choices=[('0', 'No information'), ('1', 'Some bicycle accommodation'), ('2', 'No bicycles allowed')])),
                ('extra_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('block', models.ForeignKey(blank=True, to='multigtfs.Block', help_text='Block of sequential trips that this trip belongs to.', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('route', models.ForeignKey(to='multigtfs.Route', on_delete=django.db.models.deletion.CASCADE)),
                ('service', models.ForeignKey(blank=True, to='multigtfs.Service', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('shape', models.ForeignKey(blank=True, to='multigtfs.Shape', help_text='Shape used for this trip', null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'trip',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zone_id', models.CharField(help_text='Unique identifier for a zone.', max_length=63, db_index=True)),
                ('feed', models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'zone',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stoptime',
            name='trip',
            field=models.ForeignKey(to='multigtfs.Trip', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stop',
            name='zone',
            field=models.ForeignKey(blank=True, to='multigtfs.Zone', help_text='Fare zone for a stop ID.', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='frequency',
            name='trip',
            field=models.ForeignKey(to='multigtfs.Trip', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='farerule',
            name='contains',
            field=models.ForeignKey(related_name='fare_contains', blank=True, to='multigtfs.Zone', help_text='Fare class is valid for travel withing this zone.', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='farerule',
            name='destination',
            field=models.ForeignKey(related_name='fare_destinations', blank=True, to='multigtfs.Zone', help_text='Fare class is valid for travel ending in this zone.', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='farerule',
            name='fare',
            field=models.ForeignKey(to='multigtfs.Fare', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='farerule',
            name='origin',
            field=models.ForeignKey(related_name='fare_origins', blank=True, to='multigtfs.Zone', help_text='Fare class is valid for travel originating in this zone.', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='farerule',
            name='route',
            field=models.ForeignKey(blank=True, to='multigtfs.Route', help_text='Fare class is valid for this route.', null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fare',
            name='feed',
            field=models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='block',
            name='feed',
            field=models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='feed',
            field=models.ForeignKey(to='multigtfs.Feed', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
