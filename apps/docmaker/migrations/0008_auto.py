# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field problems on 'ExerciseSet'
        db.delete_table(db.shorten_name('docmaker_exerciseset_problems'))

        # Adding M2M table for field problems_unmodified on 'ExerciseSet'
        m2m_table_name = db.shorten_name('docmaker_exerciseset_problems_unmodified')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exerciseset', models.ForeignKey(orm['docmaker.exerciseset'], null=False)),
            ('exerciseproblem', models.ForeignKey(orm['docmaker.exerciseproblem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['exerciseset_id', 'exerciseproblem_id'])


    def backwards(self, orm):
        # Adding M2M table for field problems on 'ExerciseSet'
        m2m_table_name = db.shorten_name('docmaker_exerciseset_problems')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exerciseset', models.ForeignKey(orm['docmaker.exerciseset'], null=False)),
            ('exerciseproblem', models.ForeignKey(orm['docmaker.exerciseproblem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['exerciseset_id', 'exerciseproblem_id'])

        # Removing M2M table for field problems_unmodified on 'ExerciseSet'
        db.delete_table(db.shorten_name('docmaker_exerciseset_problems_unmodified'))


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
            'Meta': {'ordering': "[u'classroom', u'activity_block', u'activity_type']", 'object_name': 'Activity'},
            'activity_block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.ActivityBlock']"}),
            'activity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.ActivityType']"}),
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['classroom.Document']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'classroom.activityblock': {
            'Meta': {'ordering': "[u'sort_order', u'week', u'weekday_index', u'heading']", 'object_name': 'ActivityBlock'},
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'week': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weekday_index': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'classroom.activitytype': {
            'Meta': {'ordering': "[u'sort_order']", 'object_name': 'ActivityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'classroom.classroom': {
            'Meta': {'ordering': "[u'-first_day']", 'object_name': 'Classroom'},
            'banner_filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
        'docmaker.docmaker': {
            'Meta': {'object_name': 'Docmaker'},
            'access_index': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'activity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.ActivityType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'template_filename': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'activity': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['classroom.Activity']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problems_unmodified': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['docmaker.ExerciseProblem']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'docmaker.exercisesetmodfication': {
            'Meta': {'ordering': "[u'exercise_set', u'problem']", 'object_name': 'ExerciseSetModfication'},
            'exercise_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docmaker.ExerciseSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'new_solution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docmaker.ExerciseProblem']"}),
            'regex_pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'regex_replace': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'activity': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['classroom.Activity']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['docmaker.LabEquipment']", 'through': "orm['docmaker.LabEquipmentRequest']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'worksheet': ('django.db.models.fields.TextField', [], {})
        },
        'docmaker.studylesson': {
            'Meta': {'object_name': 'StudyLesson'},
            'activity': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['classroom.Activity']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'banner_filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'powerpoint': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'docmaker.studyslide': {
            'Meta': {'ordering': "[u'lesson', u'sort_order']", 'object_name': 'StudySlide'},
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['docmaker.ExerciseProblem']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docmaker.StudyLesson']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['docmaker']