from __future__ import division
from __future__ import unicode_literals

from django.db.models import *

from apps.classroom.models import Classroom, Student


class AssignmentCategory(Model):
    name = CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'assignment categories'


class Assignment(Model):
    classroom = ForeignKey(Classroom)
    category = ForeignKey(AssignmentCategory)
    title = CharField(max_length=200, blank=True)
    due_date = DateField(null=True, blank=True)
    max_points = PositiveSmallIntegerField(default=0)
    curve_points = PositiveSmallIntegerField(default=0)
    is_graded = BooleanField(default=False)

    @property
    def label(self):
        return self.category
    
    @property
    def grades(self):
        return AssignmentGrade.objects.filter(assignment=self).order_by('student')
    
    def __unicode__(self):
        return '{self.label} in {self.classroom}'.format(self=self)

    class Meta:
        ordering = ['classroom', 'category', 'due_date']


class AssignmentGrade(Model):
    assignment = ForeignKey(Assignment)
    student = ForeignKey(Student)
    earned_points = PositiveSmallIntegerField(default=0)
    extra_points = PositiveSmallIntegerField(default=0)
    is_excused = BooleanField()
    note = TextField(blank=True)

    @property
    def total_points(self):
        return self.earned_points + self.extra_points + self.assignment.curve_points

    @property
    def percent(self):
        if self.assignment.max_points: # when wouldn't it be there, really?
            return self.total_points / self.assignment.max_points
        else:
            return None
        
    def __unicode__(self):
        return u'{self.assignment.label} for {self.student}'.format(self=self)


# class AssignmentGradeWeight(Model):
#     course = ForeignKey(Course)
#     title = CharField(max_length=200)
#     weight_raw = PositiveSmallIntegerField(default=1)
#
#     # gradebook = ForeignKey(Gradebook)
#     # title = CharField(max_length=20)
#     # abbr = CharField(max_length=2)
#     # weight = DecimalField(max_digits=2,decimal_places=2,help_text='Enter percent as decimal: e.g., for 20% type "0.20"')
#     # subtitle = CharField(max_length=200,blank=True)
#     # drop_worst = BooleanField(default=False)
#     # drop_best = BooleanField(default=False)
#     # if_missing_use = ForeignKey('AssignmentGradeWeight',null=True,blank=True,related_name='*')
#
#     # def csv_data(self):
#         # return '{0},{1},{2}'.format(self.abbr, self.title, self.weight)
#
#     # def __unicode__(self):
#         # label = '{0}'.format(self.title)
#         # if self.subtitle:
#             # label += ' [{0}]'.format(self.subtitle)
#         # label += ' at {0:.0%}'.format(self.weight)
#
#         # if self.drop_worst:
#             # label += ' (drop worst)'
#         # if self.drop_best:
#             # label += ' (drop best)'
#         # if self.if_missing_use:
#             # label += ' (if missing use %s)' % self.if_missing_use
#         # label = label.replace(') (',', ')
#         # return label
#
#     # class Meta:
#         # ordering = ['gradebook','-weight','drop_worst','drop_best']
#         # verbose_name_plural = 'assignment categories'
#
#     def weight(self):
#         o = self.__class__.objects.filter(course=self.course)
#         tot = sum([gw.weight_raw for gw in o])
#         return self.weight_raw / tot
#
#     def __unicode__(self):
#         return '{0} at {1:.0%}'.format(self.title, self.weight())
#
#     class Meta:
#         ordering = ['course', '-weight_raw']
#         # verbose_name_plural = 'assignment categories'

