# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table(u'photosync_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='collection_created_by', null=True, to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='collection_modified_by', null=True, to=orm['auth.User'])),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('page', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=65000, null=True, blank=True)),
        ))
        db.send_create_signal(u'photosync', ['Collection'])

        # Adding model 'PhotoSet'
        db.create_table(u'photosync_photoset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photoset_created_by', null=True, to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photoset_modified_by', null=True, to=orm['auth.User'])),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('full_path', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('total', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('farm', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('server', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('primary', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=65000, null=True, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photosets', null=True, to=orm['photosync.Collection'])),
        ))
        db.send_create_signal(u'photosync', ['PhotoSet'])

        # Adding model 'Photo'
        db.create_table(u'photosync_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photo_created_by', null=True, to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photo_modified_by', null=True, to=orm['auth.User'])),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('full_path', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('farm', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('server', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=65000, null=True, blank=True)),
            ('photoset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['photosync.PhotoSet'])),
        ))
        db.send_create_signal(u'photosync', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table(u'photosync_collection')

        # Deleting model 'PhotoSet'
        db.delete_table(u'photosync_photoset')

        # Deleting model 'Photo'
        db.delete_table(u'photosync_photo')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'photosync.collection': {
            'Meta': {'object_name': 'Collection'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '65000', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collection_created_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collection_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'photosync.photo': {
            'Meta': {'object_name': 'Photo'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_created_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '65000', 'null': 'True', 'blank': 'True'}),
            'farm': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'full_path': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'photoset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['photosync.PhotoSet']"}),
            'server': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'photosync.photoset': {
            'Meta': {'object_name': 'PhotoSet'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photosets'", 'null': 'True', 'to': u"orm['photosync.Collection']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photoset_created_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '65000', 'null': 'True', 'blank': 'True'}),
            'farm': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'full_path': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photoset_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'primary': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'server': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['photosync']