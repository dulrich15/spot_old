from __future__ import division
from __future__ import unicode_literals

from django.db.models import *
from apps.classroom.models import Classroom, Activity


docmaker_list = []


## -------------------------------------------------------------------------- ##


class CourseSyllabus(Model):
    classroom = ForeignKey(Classroom)

    @property
    def documents(self):
        return ['syllabus']

    def get_document_info(self, doc):
        context = { 
            'document_label' : 'Course Syllabus',
            'classroom': self.classroom,
        }
        template = 'latex/sy.tex'
            
        return context, template
        
    def __unicode__(self):
        return unicode(self.classroom)

    class Meta:
        verbose_name_plural = 'course syllabi'

docmaker_list.append(CourseSyllabus)


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
    # # def get_document_path(self, filename):
        # # return posixpath.join('docs', self.course.tag(), filename)

    # # def get_banner_path(self, filename):
        # # return posixpath.join('banners', self.lecture.course.tag(), filename)

    activity = ForeignKey(Activity)
    title2 = CharField(max_length=200)
    # # powerpoint = FileField(upload_to=get_document_path, storage=OverwriteStorage(), blank=True)
    # # banner = ImageField(upload_to=get_banner_path, storage=OverwriteStorage(), blank=True)
    intro = TextField(blank=True)

    @property
    def documents(self):
        return ['notes', 'examples']

    def get_examples(self):
        examples = []
        for slide in StudySlide.objects.filter(lecture=self):
            examples += slide.examples.all()
        return examples

    def get_document_info(self, doc):
        context = {
            'classroom': self.activity.classroom,
            'activity_block': self.activity.activityblock_set.all(),
            'activity': self.activity,
            'lecture': self,
        }

        if doc == 'notes':
            context['document_label'] = 'Lecture Notes'
            template = 'latex/ln.tex'
        if doc == 'examples':
            context['document_label'] = 'Lecture Examples'
            context['exercise_list'] = self.get_examples()
            context['show'] = ['answers', 'solutions']
            template = 'latex/hw.tex'
            
        return context, template
        
    def __unicode__(self):
        return '{self.activity.label}|{self.title2}'.format(self=self)


docmaker_list.append(StudyLecture)


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
        
    @property
    def documents(self):
        return ['worksheet', 'equipment']

    def get_document_info(self, doc):
        context = {
            'classroom': self.activity.classroom,
            'activity_block': self.activity.activityblock_set.all(),
            'activity': self.activity,
            'lab': self,
        }

        if doc == 'worksheet':
            context['document_label'] = 'Lab Worksheet'
            template = 'latex/lb.tex'
        if doc == 'equipment':
            context['document_label'] = 'Lab Equipment'
            template = 'latex/lf.tex'
            
        return context, template

    def __unicode__(self):
        return '{self.activity.label}|{self.title2}'.format(self=self)

docmaker_list.append(LabProject)


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
    activity = ForeignKey(Activity)
    title2 = CharField(max_length=200, blank=True)
    problems = ManyToManyField('ExerciseProblem', blank=True)

    @property
    def documents(self):
        return ['problems', 'solutions']
        
    def get_document_info(self, doc):
        context = {
            'classroom': self.activity.classroom,
            'activity_block': self.activity.activityblock_set.all(),
            'activity': self.activity,
            'exercise_list': self.problems.all(),
            'show': [],
        }
        template = 'latex/hw.tex'

        if doc == 'problems':
            context['document_label'] = 'Homework Problems'
            context['show'] = ['answers']
        if doc == 'solutions':
            context['document_label'] = 'Homework Solutions'
            context['show'] = ['answers', 'solutions']
            
        return context, template

    def __unicode__(self):
        return '{self.activity.label} | {self.title2}'.format(self=self)


docmaker_list.append(ExerciseSet)


