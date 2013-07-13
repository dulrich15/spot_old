# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Classroom'
        db.create_table('classroom_classroom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Department'])),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('first_day', self.gf('django.db.models.fields.DateField')()),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Instructor'], null=True, blank=True)),
            ('overview', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('scratchpad', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('classroom', ['Classroom'])

        # Adding model 'Department'
        db.create_table('classroom_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('classroom', ['Department'])

        # Adding model 'Instructor'
        db.create_table('classroom_instructor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('public_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('office_location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('office_hours', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('classroom', ['Instructor'])

        # Adding model 'Student'
        db.create_table('classroom_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Classroom'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('classroom', ['Student'])

        # Adding model 'Document'
        db.create_table('classroom_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Classroom'])),
            ('filepath', self.gf('django.db.models.fields.FilePathField')(path=u'c:\\Users\\Family\\Documents\\Dave\\Git repos\\github\\spot\\content\\documents', max_length=100, recursive=True, match=u'.*')),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('access_index', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('classroom', ['Document'])

        # Adding model 'ActivityType'
        db.create_table('classroom_activitytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('classroom', ['ActivityType'])

        # Adding model 'Activity'
        db.create_table('classroom_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Classroom'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.ActivityType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('classroom', ['Activity'])

        # Adding M2M table for field documents on 'Activity'
        m2m_table_name = db.shorten_name('classroom_activity_documents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['classroom.activity'], null=False)),
            ('document', models.ForeignKey(orm['classroom.document'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'document_id'])

        # Adding model 'ActivityBlock'
        db.create_table('classroom_activityblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Classroom'])),
            ('week', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('weekday_index', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('classroom', ['ActivityBlock'])

        # Adding M2M table for field activities on 'ActivityBlock'
        m2m_table_name = db.shorten_name('classroom_activityblock_activities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activityblock', models.ForeignKey(orm['classroom.activityblock'], null=False)),
            ('activity', models.ForeignKey(orm['classroom.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activityblock_id', 'activity_id'])


    def backwards(self, orm):
        # Deleting model 'Classroom'
        db.delete_table('classroom_classroom')

        # Deleting model 'Department'
        db.delete_table('classroom_department')

        # Deleting model 'Instructor'
        db.delete_table('classroom_instructor')

        # Deleting model 'Student'
        db.delete_table('classroom_student')

        # Deleting model 'Document'
        db.delete_table('classroom_document')

        # Deleting model 'ActivityType'
        db.delete_table('classroom_activitytype')

        # Deleting model 'Activity'
        db.delete_table('classroom_activity')

        # Removing M2M table for field documents on 'Activity'
        db.delete_table(db.shorten_name('classroom_activity_documents'))

        # Deleting model 'ActivityBlock'
        db.delete_table('classroom_activityblock')

        # Removing M2M table for field activities on 'ActivityBlock'
        db.delete_table(db.shorten_name('classroom_activityblock_activities'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'classroom.activity': {
            'Meta': {'object_name': 'Activity'},
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['classroom.Document']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.ActivityType']"})
        },
        'classroom.activityblock': {
            'Meta': {'ordering': "[u'sort_order', u'week', u'weekday_index', u'heading']", 'object_name': 'ActivityBlock'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['classroom.Activity']", 'null': 'True', 'blank': 'True'}),
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'week': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weekday_index': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'classroom.activitytype': {
            'Meta': {'object_name': 'ActivityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'classroom.classroom': {
            'Meta': {'ordering': "[u'-first_day']", 'object_name': 'Classroom'},
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Department']"}),
            'first_day': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Instructor']", 'null': 'True', 'blank': 'True'}),
            'overview': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'scratchpad': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'classroom.department': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Department'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'classroom.document': {
            'Meta': {'object_name': 'Document'},
            'access_index': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'filepath': ('django.db.models.fields.FilePathField', [], {'path': "u'c:\\\\Users\\\\Family\\\\Documents\\\\Dave\\\\Git repos\\\\github\\\\spot\\\\content\\\\documents'", 'max_length': '100', 'recursive': 'True', 'match': "u'.*'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'classroom.instructor': {
            'Meta': {'ordering': "[u'user__last_name', u'user__first_name']", 'object_name': 'Instructor'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office_hours': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'office_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'public_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'classroom.student': {
            'Meta': {'ordering': "[u'user__last_name', u'user__first_name']", 'object_name': 'Student'},
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['classroom']