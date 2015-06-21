# -*- coding: utf-8 -*-
# flake8: noqa
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Agency'
        db.create_table('agency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('agency_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fare_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Agency'])

        # Adding model 'Block'
        db.create_table('block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('block_id', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
        ))
        db.send_create_signal('multigtfs', ['Block'])

        # Adding model 'Fare'
        db.create_table('fare', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('fare_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=17, decimal_places=4)),
            ('currency_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('payment_method', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('transfers', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('transfer_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Fare'])

        # Adding model 'FareRule'
        db.create_table('fare_rules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fare', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Fare'])),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Route'], null=True, blank=True)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fare_origins', null=True, to=orm['multigtfs.Zone'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fare_destinations', null=True, to=orm['multigtfs.Zone'])),
            ('contains', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fare_contains', null=True, to=orm['multigtfs.Zone'])),
        ))
        db.send_create_signal('multigtfs', ['FareRule'])

        # Adding model 'FeedInfo'
        db.create_table('feed_info', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('publisher_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('publisher_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['FeedInfo'])

        # Adding model 'Frequency'
        db.create_table('frequency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Trip'])),
            ('start_time', self.gf('multigtfs.models.fields.seconds.SecondsField')()),
            ('end_time', self.gf('multigtfs.models.fields.seconds.SecondsField')()),
            ('headway_secs', self.gf('django.db.models.fields.IntegerField')()),
            ('exact_times', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Frequency'])

        # Adding model 'Route'
        db.create_table('route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('route_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Agency'], null=True, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('rtype', self.gf('django.db.models.fields.IntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('text_color', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Route'])

        # Adding model 'Service'
        db.create_table('service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('service_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('multigtfs', ['Service'])

        # Adding model 'ServiceDate'
        db.create_table('service_date', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Service'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('exception_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('multigtfs', ['ServiceDate'])

        # Adding model 'Shape'
        db.create_table('shape', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('shape_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('multigtfs', ['Shape'])

        # Adding model 'ShapePoint'
        db.create_table('shape_point', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shape', self.gf('django.db.models.fields.related.ForeignKey')(related_name='points', to=orm['multigtfs.Shape'])),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=8)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=8)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('traveled', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['ShapePoint'])

        # Adding model 'Stop'
        db.create_table('stop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('stop_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=8)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=8)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Zone'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('location_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('parent_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Stop'], null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Stop'])

        # Adding model 'Trip'
        db.create_table('trip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Route'])),
            ('trip_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('headsign', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('direction', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Block'], null=True, blank=True)),
            ('shape', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Shape'], null=True, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Trip'])

        # Adding M2M table for field services on 'Trip'
        db.create_table('trip_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trip', models.ForeignKey(orm['multigtfs.trip'], null=False)),
            ('service', models.ForeignKey(orm['multigtfs.service'], null=False))
        ))
        db.create_unique('trip_services', ['trip_id', 'service_id'])

        # Adding model 'StopTime'
        db.create_table('stop_time', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Trip'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Stop'])),
            ('arrival_time', self.gf('multigtfs.models.fields.seconds.SecondsField')(default=None, null=True, blank=True)),
            ('departure_time', self.gf('multigtfs.models.fields.seconds.SecondsField')(default=None, null=True, blank=True)),
            ('stop_sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('stop_headsign', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pickup_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('drop_off_type', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('shape_dist_traveled', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['StopTime'])

        # Adding model 'Transfer'
        db.create_table('transfer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_from_stop', to=orm['multigtfs.Stop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_to_stop', to=orm['multigtfs.Stop'])),
            ('transfer_type', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('min_transfer_time', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Transfer'])

        # Adding model 'Feed'
        db.create_table('feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('multigtfs', ['Feed'])

        # Adding model 'Zone'
        db.create_table('zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multigtfs.Feed'])),
            ('zone_id', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
        ))
        db.send_create_signal('multigtfs', ['Zone'])


    def backwards(self, orm):
        # Deleting model 'Agency'
        db.delete_table('agency')

        # Deleting model 'Block'
        db.delete_table('block')

        # Deleting model 'Fare'
        db.delete_table('fare')

        # Deleting model 'FareRule'
        db.delete_table('fare_rules')

        # Deleting model 'FeedInfo'
        db.delete_table('feed_info')

        # Deleting model 'Frequency'
        db.delete_table('frequency')

        # Deleting model 'Route'
        db.delete_table('route')

        # Deleting model 'Service'
        db.delete_table('service')

        # Deleting model 'ServiceDate'
        db.delete_table('service_date')

        # Deleting model 'Shape'
        db.delete_table('shape')

        # Deleting model 'ShapePoint'
        db.delete_table('shape_point')

        # Deleting model 'Stop'
        db.delete_table('stop')

        # Deleting model 'Trip'
        db.delete_table('trip')

        # Removing M2M table for field services on 'Trip'
        db.delete_table('trip_services')

        # Deleting model 'StopTime'
        db.delete_table('stop_time')

        # Deleting model 'Transfer'
        db.delete_table('transfer')

        # Deleting model 'Feed'
        db.delete_table('feed')

        # Deleting model 'Zone'
        db.delete_table('zone')


    models = {
        'multigtfs.agency': {
            'Meta': {'object_name': 'Agency', 'db_table': "'agency'"},
            'agency_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'fare_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'multigtfs.block': {
            'Meta': {'object_name': 'Block', 'db_table': "'block'"},
            'block_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'multigtfs.fare': {
            'Meta': {'object_name': 'Fare', 'db_table': "'fare'"},
            'currency_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'fare_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_method': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '17', 'decimal_places': '4'}),
            'transfer_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'transfers': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'multigtfs.farerule': {
            'Meta': {'object_name': 'FareRule', 'db_table': "'fare_rules'"},
            'contains': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fare_contains'", 'null': 'True', 'to': "orm['multigtfs.Zone']"}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fare_destinations'", 'null': 'True', 'to': "orm['multigtfs.Zone']"}),
            'fare': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Fare']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fare_origins'", 'null': 'True', 'to': "orm['multigtfs.Zone']"}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Route']", 'null': 'True', 'blank': 'True'})
        },
        'multigtfs.feed': {
            'Meta': {'object_name': 'Feed', 'db_table': "'feed'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'multigtfs.feedinfo': {
            'Meta': {'object_name': 'FeedInfo', 'db_table': "'feed_info'"},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'publisher_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publisher_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'multigtfs.frequency': {
            'Meta': {'object_name': 'Frequency', 'db_table': "'frequency'"},
            'end_time': ('multigtfs.models.fields.seconds.SecondsField', [], {}),
            'exact_times': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'headway_secs': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('multigtfs.models.fields.seconds.SecondsField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Trip']"})
        },
        'multigtfs.route': {
            'Meta': {'object_name': 'Route', 'db_table': "'route'"},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Agency']", 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'rtype': ('django.db.models.fields.IntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'text_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'multigtfs.service': {
            'Meta': {'object_name': 'Service', 'db_table': "'service'"},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'service_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'multigtfs.servicedate': {
            'Meta': {'object_name': 'ServiceDate', 'db_table': "'service_date'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'exception_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Service']"})
        },
        'multigtfs.shape': {
            'Meta': {'object_name': 'Shape', 'db_table': "'shape'"},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shape_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'multigtfs.shapepoint': {
            'Meta': {'object_name': 'ShapePoint', 'db_table': "'shape_point'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '8'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '8'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'shape': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points'", 'to': "orm['multigtfs.Shape']"}),
            'traveled': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'multigtfs.stop': {
            'Meta': {'object_name': 'Stop', 'db_table': "'stop'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '8'}),
            'location_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Stop']", 'null': 'True', 'blank': 'True'}),
            'stop_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Zone']", 'null': 'True', 'blank': 'True'})
        },
        'multigtfs.stoptime': {
            'Meta': {'object_name': 'StopTime', 'db_table': "'stop_time'"},
            'arrival_time': ('multigtfs.models.fields.seconds.SecondsField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'departure_time': ('multigtfs.models.fields.seconds.SecondsField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'drop_off_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'shape_dist_traveled': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Stop']"}),
            'stop_headsign': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'stop_sequence': ('django.db.models.fields.IntegerField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Trip']"})
        },
        'multigtfs.transfer': {
            'Meta': {'object_name': 'Transfer', 'db_table': "'transfer'"},
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfer_from_stop'", 'to': "orm['multigtfs.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_transfer_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfer_to_stop'", 'to': "orm['multigtfs.Stop']"}),
            'transfer_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'multigtfs.trip': {
            'Meta': {'object_name': 'Trip', 'db_table': "'trip'"},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Block']", 'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'headsign': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Route']"}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['multigtfs.Service']", 'symmetrical': 'False'}),
            'shape': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Shape']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'trip_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'multigtfs.zone': {
            'Meta': {'object_name': 'Zone', 'db_table': "'zone'"},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['multigtfs.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'})
        }
    }

    complete_apps = ['multigtfs']
