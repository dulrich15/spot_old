from __future__ import division
from __future__ import unicode_literals

from django.db.models import *
from apps.classroom.models import Activity


docmaker_list = []


class ExerciseSource(Model):
    title = CharField(max_length=200)
    author = CharField(max_length=200,blank=True)

    def __unicode__(self):
        return self.title


class ExerciseProblem(Model):
    key = SlugField()
    source = ForeignKey(ExerciseSource)

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
    problems = ManyToManyField(ExerciseProblem, blank=True)

    @property
    def documents(self):
        return ['problems', 'solutions']
        
    def get_document_info(self, doc):
        context = {
            'classroom': self.activity.classroom,
            'activity_block': self.activity.activityblock_set.all(),
            'activity': self.activity,
            'problems': self.problems,
            'show': [],
        }
        template = 'latex/hw.tex'

        if doc == 'problems':
            context['show'] = ['answers']
        if doc == 'solutions':
            context['show'] = ['answers', 'solutions']
            
        return context, template

    def __unicode__(self):
        return '{self.activity.label} | {self.title2}'.format(self=self)


docmaker_list.append(ExerciseSet)


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
            template = 'latex/lb.tex'
        if doc == 'equipment':
            template = 'latex/lf.tex'
            
        return context, template

    def __unicode__(self):
        return '{self.activity.label}|{self.title2}'.format(self=self)

docmaker_list.append(LabProject)


## -------------------------------------------------------------------------- ##


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

    def __unicode__(self):
        return '{self.activity.label}|{self.title2}'.format(self=self)


class StudySlide(Model):
    # # def get_slide_path(self, filename):
        # # return posixpath.join('slides', self.lecture.course.tag(), filename)

    lecture = ForeignKey(StudyLecture)
    sort_order = PositiveSmallIntegerField(default=0)

    title = CharField(max_length=200)
    # # image = ImageField(upload_to=get_slide_path, storage=OverwriteStorage(), blank=True)
    notes = TextField(blank=True)
    examples = ManyToManyField(ExerciseProblem, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['lecture', 'sort_order']


docmaker_list.append(StudyLecture)
