# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'activity_feed_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'activity_feed', ['User'])

        # Adding model 'Employee'
        db.create_table(u'activity_feed_employee', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activity_feed.User'], unique=True, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'activity_feed', ['Employee'])

        # Adding model 'CoffeeCompany'
        db.create_table(u'activity_feed_coffeecompany', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activity_feed.User'], unique=True, primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'activity_feed', ['CoffeeCompany'])

        # Adding model 'Activity'
        db.create_table(u'activity_feed_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'creators', to=orm['activity_feed.User'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'targets', to=orm['activity_feed.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'activity_feed', ['Activity'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'activity_feed_user')

        # Deleting model 'Employee'
        db.delete_table(u'activity_feed_employee')

        # Deleting model 'CoffeeCompany'
        db.delete_table(u'activity_feed_coffeecompany')

        # Deleting model 'Activity'
        db.delete_table(u'activity_feed_activity')


    models = {
        u'activity_feed.activity': {
            'Meta': {'object_name': 'Activity'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'creators'", 'to': u"orm['activity_feed.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'targets'", 'to': u"orm['activity_feed.User']"})
        },
        u'activity_feed.coffeecompany': {
            'Meta': {'object_name': 'CoffeeCompany', '_ormbases': [u'activity_feed.User']},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['activity_feed.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'activity_feed.employee': {
            'Meta': {'object_name': 'Employee', '_ormbases': [u'activity_feed.User']},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['activity_feed.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'activity_feed.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['activity_feed']