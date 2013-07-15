from __future__ import division
from __future__ import unicode_literals

import os
import re

from django.conf import settings

from django.db.models import *

from apps.classroom.models import ActivityType
from apps.classroom.models import Activity

from website.utils import access_choices
from website.utils import get_choices_from_path


class Docmaker(Model):
    activity_type = ForeignKey(ActivityType, null=True, blank=True)
    label = CharField(max_length=200)
    tag = CharField(max_length=2)
    template_filename = CharField(max_length=200, choices=get_choices_from_path(settings.TEMPLATE_PATH), verbose_name='template')
    access_index = PositiveSmallIntegerField(choices=access_choices, verbose_name='access', default=0)

    @property
    def access(self):
        return access_choices[self.access_index][1]

    @property
    def template(self):
        return os.path.join(settings.TEMPLATE_PATH, self.template_filename)

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
        
        def __unicode__(self):
            if self.activity and self.title:
                return '{self.activity.label}: {self.title}'.format(self=self)
            elif self.activity:
                return self.activity.label
            elif self.title:
                return self.title
            else:
                return '{self.__class__.__name__} #{self.pk}'.format(self=self)
                
        builder.__unicode__ = __unicode__
                
context_builders = ContextBuilderCollection()

from apps.classroom.models import Activity
def title(self):
    for model in context_builders.models:
        try:
            obj = model.objects.get(activity=self)
            return obj.title
        except:
            pass
    return ''
Activity.title = title


## -------------------------------------------------------------------------- ##


class StudySlide(Model):
    lesson = ForeignKey('StudyLesson')
    sort_order = PositiveSmallIntegerField(default=0)

    title = CharField(max_length=200)
    image_filename = CharField(max_length=200, choices=get_choices_from_path(settings.SLIDE_PATH), null=True, blank=True)
    notes = TextField(blank=True)
    examples = ManyToManyField('ExerciseProblem', blank=True)

    @property
    def image(self):
        image = {}
        image['name'] = self.image_filename
        image['path'] = os.path.join(settings.SLIDE_PATH, image['name'])
        image['exists'] = os.path.isfile(image['path']),
        # image['url'] = '/'.join(settings.SLIDE_URL, image['name']),
        return image
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['lesson', 'sort_order']


class StudyLesson(Model):
    activity = OneToOneField(Activity, null=True, blank=True)
    title = CharField(max_length=200)
    powerpoint = CharField(max_length=200, choices=get_choices_from_path(settings.DOCUMENT_PATH, filter='*.ppt'), null=True, blank=True)
    banner_filename = CharField(max_length=200, choices=get_choices_from_path(settings.BANNER_PATH), null=True, blank=True)
    intro = TextField(blank=True)

    @property
    def banner(self):
        banner = {}
        banner['name'] = self.banner_filename
        banner['path'] = os.path.join(settings.BANNER_PATH, banner['name'])
        banner['exists'] = os.path.isfile(banner['path']),
        # banner['url'] = '/'.join(settings.SLIDE_URL, banner['name']),
        return banner
        
    def get_examples(self):
        examples = []
        for slide in StudySlide.objects.filter(lesson=self):
            examples += slide.examples.all()
        return examples

    @property
    def extra_context(self):
        return {'lecture': self, 'exercise_list': self.get_examples()}

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


class ExerciseSetModfication(Model):
    exercise_set = ForeignKey('ExerciseSet')
    problem = ForeignKey('ExerciseProblem')
    regex_pattern = CharField(max_length=200)
    regex_replace = CharField(max_length=200)
    sort_order = PositiveSmallIntegerField(default=0)
    new_answer = TextField(blank=True)
    new_solution = TextField(blank=True)
    
    def __unicode__(self):
        return '{self.exercise_set}: {self.problem.key}'.format(self=self)
        
    class Meta:
        ordering = ['exercise_set', 'problem']

        
class ExerciseSet(Model):
    activity = OneToOneField(Activity, null=True, blank=True)
    title = CharField(max_length=200, blank=True)
    problems_unmodified = ManyToManyField('ExerciseProblem', verbose_name='problems', blank=True)

    @property
    def problems(self):
        print "hi"
        problems = []
        for problem in self.problems_unmodified.all():
            print problem
            key = problem.key
            question = problem.question
            answer = problem.answer
            solution = problem.solution

            mods = ExerciseSetModfication.objects.filter(exercise_set=self, problem=problem)
            for mod in mods:
                pattern = mod.regex_pattern
                repl = mod.regex_replace
                key = '{} modified'.format(problem.key)
                question = re.sub(pattern, repl, question)
                answer = mod.new_answer
                solution = mod.new_solution

            if not answer:
                answer = 'TBD'
                
            if not solution:
                solution = 'No solution available.'
                
            problems.append({
                'key': key,
                'question': question,
                'answer': answer,
                'solution': solution,
            })
        print problems
        return problems

    
    @property
    def extra_context(self):
        return {'exercise_list': self.problems}

context_builders.register(ExerciseSet)
