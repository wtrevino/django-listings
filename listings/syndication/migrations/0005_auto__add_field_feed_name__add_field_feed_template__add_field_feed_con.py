# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Feed.name'
        db.add_column('syndication_feed', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=100),
                      keep_default=False)

        # Adding field 'Feed.template'
        db.add_column('syndication_feed', 'template',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Feed.content_type'
        db.add_column('syndication_feed', 'content_type',
                      self.gf('django.db.models.fields.CharField')(default='application/xml', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Feed.name'
        db.delete_column('syndication_feed', 'name')

        # Deleting field 'Feed.template'
        db.delete_column('syndication_feed', 'template')

        # Deleting field 'Feed.content_type'
        db.delete_column('syndication_feed', 'content_type')


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
            'feed_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['syndication.FeedType']"}),
            'feed_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
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