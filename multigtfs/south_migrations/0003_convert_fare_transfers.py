# -*- coding: utf-8 -*-
# flake8: noqa
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        orm['multigtfs.fare'].objects.filter(transfers=-1).update(transfers=None)

    def backwards(self, orm):
        orm['multigtfs.fare'].objects.filter(transfers=None).update(transfers=-1)

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
            'transfers': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
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
    symmetrical = True
