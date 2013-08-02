from __future__ import division
from __future__ import unicode_literals

from django.db.models import *

from apps.classroom.models import Classroom, Student


class AssignmentCategory(Model):
    label = CharField(max_length=200)

    def __unicode__(self):
        return self.label

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
    def nbr(self):
        x = self.__class__.objects.filter(classroom=self.classroom, category=self.category)
        x = sorted(x, key=lambda a: a.due_date)
        return x.index(self) + 1

    @property
    def label(self):
        if self.title:
            return self.title
        else:
            return '{self.category} {self.nbr}'.format(self=self)

    @property
    def grades(self):
        grades = []
        for student in Student.objects.filter(classroom=self.classroom):
            try:
                grade = AssignmentGrade.objects.get(assignment=self, student=student)
            except:
                class grade(object):
                    pass
            grade.student = student
            grades.append(grade)
        return grades

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
        return '{self.assignment.label} for {self.student}'.format(self=self)


class GradeScheme(Model):
    classroom = OneToOneField(Classroom)
    notes = TextField(blank=True)

    def __unicode__(self):
        return '{self.classroom}'.format(self=self)

    class Meta:
        ordering = ['classroom']


class GradeWeight(Model):
    scheme = ForeignKey('GradeScheme')
    category = OneToOneField(AssignmentCategory)
    weight_raw = PositiveSmallIntegerField(default=1)

    # if_missing_use = ForeignKey('AssignmentGradeWeight',null=True,blank=True,related_name='*')
    # drop_worst = BooleanField(default=False)
    # drop_best = BooleanField(default=False)
    # notes = TextField(null=True, blank=True)

    @property
    def weight(self):
        o = self.__class__.objects.filter(scheme=self.scheme)
        tot = sum([gw.weight_raw for gw in o])
        return self.weight_raw / tot

    def __unicode__(self):
        return '{self.category.label} at {self.weight:.0%}'.format(self=self)

    class Meta:
        ordering = ['scheme', '-weight_raw', 'category']
