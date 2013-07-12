# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ClassroomSyllabus'
        db.delete_table('docmaker_classroomsyllabus')

        # Adding model 'Syllabus'
        db.create_table('docmaker_syllabus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Classroom'])),
        ))
        db.send_create_signal('docmaker', ['Syllabus'])


    def backwards(self, orm):
        # Adding model 'ClassroomSyllabus'
        db.create_table('docmaker_classroomsyllabus', (
            ('classroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Classroom'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('docmaker', ['ClassroomSyllabus'])

        # Deleting model 'Syllabus'
        db.delete_table('docmaker_syllabus')


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
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'filepath': ('django.db.models.fields.FilePathField', [], {'path': "u'C:\\\\Program Files\\\\my\\\\github\\\\spot\\\\content\\\\documents'", 'max_length': '100', 'recursive': 'True', 'match': "u'.*'"}),
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'docmaker.exerciseproblem': {
            'Meta': {'ordering': "[u'key']", 'object_name': 'ExerciseProblem'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'solution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docmaker.ExerciseSource']"})
        },
        'docmaker.exerciseset': {
            'Meta': {'object_name': 'ExerciseSet'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problems': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['docmaker.ExerciseProblem']", 'symmetrical': 'False', 'blank': 'True'}),
            'title2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'docmaker.exercisesource': {
            'Meta': {'object_name': 'ExerciseSource'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'docmaker.labequipment': {
            'Meta': {'ordering': "[u'item']", 'object_name': 'LabEquipment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'docmaker.labequipmentrequest': {
            'Meta': {'ordering': "[u'equipment__location']", 'object_name': 'LabEquipmentRequest'},
            'equipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docmaker.LabEquipment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docmaker.LabProject']"}),
            'quantity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'docmaker.labproject': {
            'Meta': {'object_name': 'LabProject'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Activity']"}),
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['docmaker.LabEquipment']", 'through': "orm['docmaker.LabEquipmentRequest']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title2': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'worksheet': ('django.db.models.fields.TextField', [], {})
        },
        'docmaker.studylecture': {
            'Meta': {'object_name': 'StudyLecture'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title2': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'docmaker.studyslide': {
            'Meta': {'ordering': "[u'lecture', u'sort_order']", 'object_name': 'StudySlide'},
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['docmaker.ExerciseProblem']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docmaker.StudyLecture']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'docmaker.syllabus': {
            'Meta': {'object_name': 'Syllabus'},
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['docmaker']