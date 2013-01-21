# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FeedType'
        db.create_table('syndication_feedtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('template', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('content_type', self.gf('django.db.models.fields.CharField')(default='Content-type: application/xml', unique=True, max_length=100)),
        ))
        db.send_create_signal('syndication', ['FeedType'])

        # Adding model 'Feed'
        db.create_table('syndication_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syndication.FeedType'])),
        ))
        db.send_create_signal('syndication', ['Feed'])

        # Adding M2M table for field site on 'Feed'
        db.create_table('syndication_feed_site', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm['syndication.feed'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('syndication_feed_site', ['feed_id', 'site_id'])


    def backwards(self, orm):
        # Deleting model 'FeedType'
        db.delete_table('syndication_feedtype')

        # Deleting model 'Feed'
        db.delete_table('syndication_feed')

        # Removing M2M table for field site on 'Feed'
        db.delete_table('syndication_feed_site')


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
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'Content-type: application/xml'", 'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['syndication']