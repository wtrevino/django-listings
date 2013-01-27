# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Feed.feed_type'
        db.delete_column('syndication_feed', 'feed_type_id')


    def backwards(self, orm):
        # Adding field 'Feed.feed_type'
        db.add_column('syndication_feed', 'feed_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['syndication.FeedType']),
                      keep_default=False)


    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'syndication.feed': {
            'Meta': {'object_name': 'Feed'},
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'application/xml'", 'max_length': '100'}),
            'feed_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'syndication.feedtype': {
            'Meta': {'object_name': 'FeedType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['syndication']