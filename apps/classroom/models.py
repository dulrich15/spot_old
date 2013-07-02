from __future__ import division
from __future__ import unicode_literals

import copy
import datetime
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import *

weekday_choices = (
    (0, 'Mon'),
    (1, 'Tue'),
    (2, 'Wed'),
    (3, 'Thu'),
    (4, 'Fri'),
    (5, 'Sat'),
    (6, 'Sun'),
)

class Instructor(Model):
    user = ForeignKey(User)
    public_name = CharField(max_length=200, blank=True)
    office_location = CharField(max_length=200, blank=True)
    office_hours = CharField(max_length=200, blank=True)
    email = EmailField(blank=True)
    website = URLField(blank=True)

    def get_public_name(self):
        if self.public_name:
            return self.public_name
        else:
            return self.user.get_full_name()
        
    def __unicode__(self):
        return self.get_public_name()

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class Department(Model):
    name = CharField(max_length=200, blank=True)
    abbr = CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Classroom(Model):
    dept = ForeignKey(Department)
    term = CharField(max_length=200)
    first_day = DateField()
    
    subtitle = CharField(max_length=200, blank=True)
    instructor = ForeignKey(Instructor, null=True, blank=True)

    overview = TextField(blank=True)
    scratchpad = TextField(blank=True)

    @property
    def title(self):
        return '{self.dept} {self.term}'.format(self=self)
        
    @property
    def slug(self):
        return '{self.dept.abbr}{self.term}'.format(self=self)

    @property
    def lib(self):
        return '{self.slug} {self.first_day}'.format(self=self)
    
    @property
    def document_path(self):
        return os.path.join(settings.MEDIA_ROOT, 'classroom', self.lib)
        
    @property
    def year(self):
        return self.first_day.year

    @property
    def season(self): # notice: June should be *summer* term
        return ['Winter','Spring','Summer','Fall'][int((self.first_day.month + 1)/ 3)]
        
    def copy_instance(self):
        instance = copy.deepcopy(self)
        instance.id = None
        instance.save()

    def __unicode__(self):
        return '{self.title}, {self.season} {self.year}'.format(self=self)

    class Meta:
        ordering = ['-first_day']

        
class Student(Model):
    classroom = ForeignKey(Classroom)
    user = ForeignKey(User)
        
    @property
    def last_name(self):
        return self.user.last_name

    @property
    def first_name(self):
        return self.user.first_name
        
    def __unicode__(self):
        return '{self.last_name}, {self.first_name} in {self.classroom}'.format(self=self)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class Activity(Model):
    classroom = ForeignKey(Classroom)
    label = CharField(max_length=200)
    
    def __unicode__(self):
        return self.label


class ActivityBlock(Model):
    classroom = ForeignKey(Classroom)
    week = PositiveSmallIntegerField(null=True, blank=True)
    weekday_index = PositiveSmallIntegerField(choices=weekday_choices, verbose_name='weekday', null=True, blank=True)
    heading = CharField(max_length=200, null=True, blank=True)
    sort_order = PositiveSmallIntegerField(null=True, blank=True)
    activities = ManyToManyField(Activity, null=True, blank=True)
    
    @property
    def weekday(self):
        if self.weekday_index is not None:
            return weekday_choices[self.weekday_index][1]
        else:
            return None
    
    @property
    def date(self):
        if self.classroom.first_day and self.week and self.weekday:
            return self.classroom.first_day + datetime.timedelta(7 * (self.week - 1) + self.weekday_index)
        else:
            return None

    def __unicode__(self):
        if self.date:
            return '{self.weekday} Week {self.week}'.format(self=self)
        elif self.week:
            return 'Week {self.week}'.format(self=self)
        elif self.heading:
            return self.heading
        else:
            return 'Block id {self.id}'.format(self=self)
            
    class Meta:
        ordering = ['sort_order', 'week', 'weekday_index', 'heading']


# class Activity(Model):
#     block = ForeignKey(ActivityBlock)
#     label = CharField(max_length=200)
#     
#     @property
#     def classroom(self):
#         return self.block.classroom
#         
#     def __unicode__(self):
#         return '{self.label} from {self.classroom}'.format(self=self)


