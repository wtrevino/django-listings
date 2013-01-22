# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'FeedType', fields ['content_type']
        db.delete_unique('syndication_feedtype', ['content_type'])


    def backwards(self, orm):
        # Adding unique constraint on 'FeedType', fields ['content_type']
        db.create_unique('syndication_feedtype', ['content_type'])


    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'syndication.feed': {
            'Meta': {'object_name': 'Feed'},
            'feed_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['syndication.FeedType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        },
        'syndication.feedtype': {
            'Meta': {'object_name': 'FeedType'},
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'application/xml'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['syndication']