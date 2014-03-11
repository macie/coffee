# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        EMPLOYEES = ({'first_name': 'Jan',
                      'last_name': 'Kowalski'},
                     {'first_name': 'Adam',
                      'last_name': 'Nowak'},
                     {'first_name': 'Anna',
                      'last_name': 'Wiśniewska'}, )
        COFFEE_COMPANIES = ({'full_name': 'KawEx'},
                            {'full_name': 'Coffeepol'}, )

        for employee in EMPLOYEES:
            orm.Employee.objects.create(
                first_name=employee['first_name'],
                last_name=employee['last_name'])

        for company in COFFEE_COMPANIES:
            orm.CoffeeCompany.objects.create(
                full_name=company['full_name'])

    def backwards(self, orm):
        "Write your backwards methods here."

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
    symmetrical = True
