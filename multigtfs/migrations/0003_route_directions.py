# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0002_add_on_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteDirection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(blank=True, choices=[('0', '0'), ('1', '1')], help_text='Direction of travel for direction description.', max_length=1)),
                ('direction_name', models.CharField(blank=True, help_text='Destination identification for passengers.', max_length=255)),
                ('extra_data', jsonfield.fields.JSONField(blank=True, default={}, null=True)),
                ('route', models.ForeignKey(blank=True, help_text='Route for which this direction description applies.', null=True, on_delete=django.db.models.deletion.CASCADE, to='multigtfs.Route')),
            ],
            options={
                'db_table': 'route_directions',
            },
        ),
    ]
