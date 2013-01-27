# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FeedType.template'
        db.delete_column('syndication_feedtype', 'template')

        # Deleting field 'FeedType.content_type'
        db.delete_column('syndication_feedtype', 'content_type')

        # Deleting field 'FeedType.name'
        db.delete_column('syndication_feedtype', 'name')


    def backwards(self, orm):
        # Adding field 'FeedType.template'
        db.add_column('syndication_feedtype', 'template',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'FeedType.content_type'
        db.add_column('syndication_feedtype', 'content_type',
                      self.gf('django.db.models.fields.CharField')(default='application/xml', max_length=100),
                      keep_default=False)

        # Adding field 'FeedType.name'
        db.add_column('syndication_feedtype', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, unique=True),
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
            'feed_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['syndication.FeedType']"}),
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