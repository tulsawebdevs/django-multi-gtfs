# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farerule',
            name='contains',
            field=models.ForeignKey(blank=True, null=True, help_text='Fare class is valid for travel withing this zone.', related_name='fare_contains', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Zone'),
        ),
        migrations.AlterField(
            model_name='farerule',
            name='destination',
            field=models.ForeignKey(blank=True, null=True, help_text='Fare class is valid for travel ending in this zone.', related_name='fare_destinations', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Zone'),
        ),
        migrations.AlterField(
            model_name='farerule',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, help_text='Fare class is valid for travel originating in this zone.', related_name='fare_origins', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Zone'),
        ),
        migrations.AlterField(
            model_name='farerule',
            name='route',
            field=models.ForeignKey(blank=True, null=True, help_text='Fare class is valid for this route.', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Route'),
        ),
        migrations.AlterField(
            model_name='route',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, help_text='Agency for this route.', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Agency'),
        ),
        migrations.AlterField(
            model_name='stop',
            name='parent_station',
            field=models.ForeignKey(blank=True, null=True, help_text='The station associated with the stop', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Stop'),
        ),
        migrations.AlterField(
            model_name='stop',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, help_text='Fare zone for a stop ID.', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Zone'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='block',
            field=models.ForeignKey(blank=True, null=True, help_text='Block of sequential trips that this trip belongs to.', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Block'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Service'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='shape',
            field=models.ForeignKey(blank=True, null=True, help_text='Shape used for this trip', on_delete=django.db.models.deletion.SET_NULL, to='multigtfs.Shape'),
        ),
    ]
