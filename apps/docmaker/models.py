from __future__ import division
from __future__ import unicode_literals

import os

from django.db.models import *
from apps.classroom.models import Classroom, Activity, ActivityType


class DocmakerCollection(object):
    types = []
        
    def register(self, docmaker):
        self.types.append(docmaker)

        @property
        def objects(self):
            try:
                return docmaker.objects.filter(classroom=classroom)
            except:
                return docmaker.objects.filter(activity__classroom=classroom)
            
        docmaker.objects = objects
        docmaker.label = docmaker._meta.verbose_name_plural
        
    @property
    def choices(self):
        choices = ()
        for type in self.types:
            choices += ((self.types.index(type), type.label),)
        return choices
            
    @property
    def docs(self):
        docs = {}
        for doctag in self.__class__.doctags:
            context = self.get_context(doctag)
            template = Template.objects.get(activity_type=self.activity.type).latex
            docs[doctag] = { 'context': context, 'template': template }
        return docs

docmakers = DocmakerCollection()


## -------------------------------------------------------------------------- ##


class CourseSyllabus(Model):
    doctags = ['sy']

    classroom = ForeignKey(Classroom)

    def get_context(self, doctag):
        context = {
            'document_label' : 'Course Syllabus',
            'classroom': self.classroom,
        }

    @property
    def docs(self):
        docs = {}
        for doctag in self.__class__.doctags:
            context = self.get_context(doctag)
            template = 'latex/sy.tex' ############################################################
            docs[doctag] = { 'context': context, 'template': template }
        return docs

    def __unicode__(self):
        return unicode(self.classroom)

    class Meta:
        verbose_name_plural = 'course syllabi'

docmakers.register(CourseSyllabus)


## -------------------------------------------------------------------------- ##


class StudySlide(Model):
    # # def get_slide_path(self, filename):
        # # return posixpath.join('slides', self.lecture.course.tag(), filename)

    lecture = ForeignKey('StudyLecture')
    sort_order = PositiveSmallIntegerField(default=0)

    title = CharField(max_length=200)
    # # image = ImageField(upload_to=get_slide_path, storage=OverwriteStorage(), blank=True)
    notes = TextField(blank=True)
    examples = ManyToManyField('ExerciseProblem', blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['lecture', 'sort_order']


class StudyLecture(Model):
    doctags = ['ln', 'lx']

    # # def get_document_path(self, filename):
        # # return posixpath.join('documents', self.course.tag(), filename)

    # # def get_banner_path(self, filename):
        # # return posixpath.join('banners', self.lecture.course.tag(), filename)

    activity = ForeignKey(Activity)
    title2 = CharField(max_length=200)
    # # powerpoint = FileField(upload_to=get_document_path, storage=OverwriteStorage(), blank=True)
    # # banner = ImageField(upload_to=get_banner_path, storage=OverwriteStorage(), blank=True)
    intro = TextField(blank=True)

    def get_examples(self):
        examples = []
        for slide in StudySlide.objects.filter(lecture=self):
            examples += slide.examples.all()
        return examples

    def get_context(self, doctag):
        context = {
            'classroom': self.activity.classroom,
            'activity_block': self.activity.activityblock_set.all(),
            'activity': self.activity,
            'lecture': self,
        }

        if doctag == 'ln':
            context['document_label'] = 'Lecture Notes'

        if doctag == 'lx':
            context['document_label'] = 'Lecture Examples'
            context['exercise_list'] = self.get_examples()
            context['show'] = ['answers', 'solutions']

        return context

    def __unicode__(self):
        return '{self.activity.label} | {self.title2}'.format(self=self)


docmakers.register(StudyLecture)


## -------------------------------------------------------------------------- ##


class LabEquipment(Model):
    item = CharField(max_length=200)
    location = CharField(max_length=200)

    def __unicode__(self):
        return self.item

    class Meta:
        verbose_name_plural = 'lab equipment'
        ordering = ['item']


class LabEquipmentRequest(Model):
    lab = ForeignKey('LabProject')
    equipment = ForeignKey('LabEquipment')
    quantity = PositiveSmallIntegerField(blank=True,null=True)

    def __unicode__(self):
        if self.quantity:
            return '{self.quantity} {self.equipment.item}'.format(self=self)
        else:
            return self.equipment.item

    class Meta:
        ordering = ['equipment__location']


class LabProject(Model):
    doctags = ['lb', 'lf']

    activity = ForeignKey(Activity)
    title2 = CharField(max_length=200)
    worksheet = TextField()
    notes = TextField(blank=True)
    equipment = ManyToManyField(LabEquipment, through='LabEquipmentRequest')

    @property
    def notes_list(self):
        notes_list = self.notes.splitlines()
        if len(notes_list) < 3:
            notes_list += (3 - len(notes_list))*['']
        return notes_list

    def get_context(self, doctag):
        context = {
            'classroom': self.activity.classroom,
            'activity_block': self.activity.activityblock_set.all(),
            'activity': self.activity,
            'lab': self,
        }

        if doctag == 'lb':
            context['document_label'] = 'Lab Worksheet'

        if doctag == 'lf':
            context['document_label'] = 'Lab Equipment'

        return context
    @property
    def docs(self):
        docs = {}
        for doctag in self.__class__.doctags:
            context = self.get_context(doctag)
            template = Template.objects.get(activity_type=self.activity.type).latex
            docs[doctag] = { 'context': context, 'template': template }
        return docs

    def __unicode__(self):
        return '{self.activity.label} | {self.title2}'.format(self=self)

docmakers.register(LabProject)


## -------------------------------------------------------------------------- ##


class ExerciseSource(Model):
    title = CharField(max_length=200)
    author = CharField(max_length=200,blank=True)

    def __unicode__(self):
        return self.title


class ExerciseProblem(Model):
    key = SlugField()
    source = ForeignKey('ExerciseSource')

    question = TextField()
    answer = TextField(blank=True)
    solution = TextField(blank=True)
    notes = TextField(blank=True)

    @property
    def title(self):
        if len(self.question) > 97:
            return self.question[:97] + '...'
        else:
            return self.question

    def __unicode__(self):
        return '[{self.key}] {self.title}'.format(self=self)

    class Meta:
        ordering = ['key']


class ExerciseSet(Model):
    doctags = ['hp', 'hs']

    activity = ForeignKey(Activity)
    title2 = CharField(max_length=200, blank=True)
    problems = ManyToManyField('ExerciseProblem', blank=True)

    def get_context(self, doctag):
        context = {
            'classroom': self.activity.classroom,
            'activity_block': self.activity.activityblock_set.all(),
            'activity': self.activity,
            'exercise_list': self.problems.all(),
            'show': [],
        }

        if doctag == 'hp':
            context['document_label'] = 'Homework Problems'
            context['show'] = ['answers']

        if doctag == 'hs':
            context['document_label'] = 'Homework Solutions'
            context['show'] = ['answers', 'solutions']

        return context
        
    @property
    def docs(self):
        docs = {}
        for doctag in self.__class__.doctags:
            context = self.get_context(doctag)
            template = Template.objects.get(activity_type=self.activity.type).latex
            docs[doctag] = { 'context': context, 'template': template }
        return docs

    def __unicode__(self):
        return '{self.activity.label} | {self.title2}'.format(self=self)


docmakers.register(ExerciseSet)


## -------------------------------------------------------------------------- ##


class DocumentType(Model):
    template_path = os.path.join(settings.PROJECT_PATH, 'apps', 'docmaker', 'templates', 'latex')

    label = CharField(max_length=200, blank=True)
    activity_type = ForeignKey(ActivityType, null=True, blank=True)
    context_source = PositiveSmallIntegerField(choices=docmakers.choices)
    template_latex = FilePathField(path=template_path, match='.tex')
#     latex = TextBox(null=True, blank=True)
#     html = TextBox(null=True, blank=True)