from __future__ import division
from __future__ import unicode_literals

import os

from django.db.models import *
from apps.classroom.models import ActivityType, Activity, access_choices

from website.utils import get_choices_from_list
from website.utils import get_choices_from_path


class Docmaker(Model):
    template_path = os.path.join(settings.PROJECT_PATH, 'apps', 'docmaker', 'templates', 'latex')

    activity_type = ForeignKey(ActivityType, null=True, blank=True)
    label = CharField(max_length=200)
    tag = CharField(max_length=2)
    template_filename = CharField(max_length=200, choices=get_choices_from_path(template_path), verbose_name='template')
    access_index = PositiveSmallIntegerField(choices=access_choices, verbose_name='access', default=0)

    @property
    def access(self):
        return access_choices[self.access_index][1]

    @property
    def template(self):
        return os.path.join(Docmaker.template_path, self.template_filename)

    @property
    def filename(self):
        return os.path.split(self.template)[1]

    def __unicode__(self):
        return self.label


## -------------------------------------------------------------------------- ##


class ContextBuilderCollection(object):
    models = []

    def register(self, builder):
        self.models.append(builder)

context_builders = ContextBuilderCollection()


## -------------------------------------------------------------------------- ##


class StudySlide(Model):
    # # def get_slide_path(self, filename):
        # # return posixpath.join('slides', self.lecture.course.tag(), filename)

    lesson = ForeignKey('StudyLesson')
    sort_order = PositiveSmallIntegerField(default=0)

    title = CharField(max_length=200)
    # # image = ImageField(upload_to=get_slide_path, storage=OverwriteStorage(), blank=True)
    notes = TextField(blank=True)
    examples = ManyToManyField('ExerciseProblem', blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['lesson', 'sort_order']


class StudyLesson(Model):
    # # def get_document_path(self, filename):
        # # return posixpath.join('documents', self.course.tag(), filename)

    # # def get_banner_path(self, filename):
        # # return posixpath.join('banners', self.lecture.course.tag(), filename)

    activity = OneToOneField(Activity, null=True, blank=True)
    title = CharField(max_length=200)
    # # powerpoint = FileField(upload_to=get_document_path, storage=OverwriteStorage(), blank=True)
    # # banner = ImageField(upload_to=get_banner_path, storage=OverwriteStorage(), blank=True)
    intro = TextField(blank=True)

    def get_examples(self):
        examples = []
        for slide in StudySlide.objects.filter(lesson=self):
            examples += slide.examples.all()
        return examples

    @property
    def extra_context(self):
        return {'lecture': self, 'exercise_list': self.get_examples()}

    def __unicode__(self):
        return '{self.activity.label} | {self.title}'.format(self=self)


context_builders.register(StudyLesson)


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
    activity = OneToOneField(Activity, null=True, blank=True)
    title = CharField(max_length=200)
    worksheet = TextField()
    notes = TextField(blank=True)
    equipment = ManyToManyField(LabEquipment, through='LabEquipmentRequest')

    @property
    def notes_list(self):
        notes_list = self.notes.splitlines()
        if len(notes_list) < 3:
            notes_list += (3 - len(notes_list))*['']
        return notes_list

    @property
    def extra_context(self):
        return {'lab': self}

    def __unicode__(self):
        return '{self.activity.label} | {self.title}'.format(self=self)


context_builders.register(LabProject)


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
    activity = OneToOneField(Activity, null=True, blank=True)
    title = CharField(max_length=200, blank=True)
    problems = ManyToManyField('ExerciseProblem', blank=True)

    @property
    def extra_context(self):
        return {'exercise_list': self.problems.all()}

    def __unicode__(self):
        return '{self.activity.label} | {self.title}'.format(self=self)


context_builders.register(ExerciseSet)
