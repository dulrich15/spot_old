# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AssignmentCategory'
        db.create_table('gradebook_assignmentcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('gradebook', ['AssignmentCategory'])

        # Adding model 'Assignment'
        db.create_table('gradebook_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classroom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Classroom'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradebook.AssignmentCategory'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('max_points', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('curve_points', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('is_graded', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gradebook', ['Assignment'])

        # Adding model 'AssignmentGrade'
        db.create_table('gradebook_assignmentgrade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradebook.Assignment'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classroom.Student'])),
            ('earned_points', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('extra_points', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('is_excused', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('gradebook', ['AssignmentGrade'])

        # Adding model 'GradeScheme'
        db.create_table('gradebook_gradescheme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classroom', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['classroom.Classroom'], unique=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('gradebook', ['GradeScheme'])

        # Adding model 'GradeWeight'
        db.create_table('gradebook_gradeweight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradebook.GradeScheme'])),
            ('category', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gradebook.AssignmentCategory'], unique=True)),
            ('weight_raw', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('gradebook', ['GradeWeight'])


    def backwards(self, orm):
        # Deleting model 'AssignmentCategory'
        db.delete_table('gradebook_assignmentcategory')

        # Deleting model 'Assignment'
        db.delete_table('gradebook_assignment')

        # Deleting model 'AssignmentGrade'
        db.delete_table('gradebook_assignmentgrade')

        # Deleting model 'GradeScheme'
        db.delete_table('gradebook_gradescheme')

        # Deleting model 'GradeWeight'
        db.delete_table('gradebook_gradeweight')


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
        'classroom.classroom': {
            'Meta': {'ordering': "[u'-first_day']", 'object_name': 'Classroom'},
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Department']"}),
            'first_day': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Instructor']", 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        },
        'gradebook.assignment': {
            'Meta': {'ordering': "[u'classroom', u'category', u'due_date']", 'object_name': 'Assignment'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradebook.AssignmentCategory']"}),
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Classroom']"}),
            'curve_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_graded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'gradebook.assignmentcategory': {
            'Meta': {'object_name': 'AssignmentCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'gradebook.assignmentgrade': {
            'Meta': {'object_name': 'AssignmentGrade'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradebook.Assignment']"}),
            'earned_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'extra_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_excused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classroom.Student']"})
        },
        'gradebook.gradescheme': {
            'Meta': {'ordering': "[u'classroom']", 'object_name': 'GradeScheme'},
            'classroom': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['classroom.Classroom']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'gradebook.gradeweight': {
            'Meta': {'ordering': "[u'scheme', u'-weight_raw', u'category']", 'object_name': 'GradeWeight'},
            'category': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gradebook.AssignmentCategory']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradebook.GradeScheme']"}),
            'weight_raw': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['gradebook']