# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'event'
        db.create_table(u'pyEventOrderWeb_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('event_detail', self.gf('django.db.models.fields.TextField')(max_length=100000)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('event_registdeadline', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('event_hostfakeID', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('event_hostname', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('event_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('event_sn', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'pyEventOrderWeb', ['event'])

        # Adding model 'participant'
        db.create_table(u'pyEventOrderWeb_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partici_fakeID', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('event_ID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyEventOrderWeb.event'])),
            ('event_sn', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('partici_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('partici_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'pyEventOrderWeb', ['participant'])

        # Adding model 'wechat_user'
        db.create_table(u'pyEventOrderWeb_wechat_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wechat_fakeID', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wechat_username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wechat_inputname', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('wechat_usertype', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'pyEventOrderWeb', ['wechat_user'])


    def backwards(self, orm):
        # Deleting model 'event'
        db.delete_table(u'pyEventOrderWeb_event')

        # Deleting model 'participant'
        db.delete_table(u'pyEventOrderWeb_participant')

        # Deleting model 'wechat_user'
        db.delete_table(u'pyEventOrderWeb_wechat_user')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pyEventOrderWeb.event': {
            'Meta': {'object_name': 'event'},
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_detail': ('django.db.models.fields.TextField', [], {'max_length': '100000'}),
            'event_hostfakeID': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'event_hostname': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'event_limit': ('django.db.models.fields.IntegerField', [], {}),
            'event_registdeadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_sn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'event_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'})
        },
        u'pyEventOrderWeb.participant': {
            'Meta': {'object_name': 'participant'},
            'event_ID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyEventOrderWeb.event']"}),
            'event_sn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partici_fakeID': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'partici_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'partici_type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'pyEventOrderWeb.wechat_user': {
            'Meta': {'object_name': 'wechat_user'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wechat_fakeID': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wechat_inputname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'wechat_username': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wechat_usertype': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['pyEventOrderWeb']