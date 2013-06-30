from __future__ import division
from __future__ import unicode_literals

import copy

from django.contrib.auth.models import User
from django.db.models import *


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
    is_active = BooleanField(default=True)
    first_day = DateField()
    dept = ForeignKey(Department)
    term = CharField(max_length=200)
    
    subtitle = CharField(max_length=200, blank=True)
    overview = TextField(blank=True)
    outline = TextField(blank=True)

    instructor = ForeignKey(Instructor, null=True, blank=True)
    scratchpad = TextField(blank=True)

    @property
    def title(self):
        return '{self.dept} {self.term}'.format(self=self)
        
    @property
    def slug(self):
        '{self.dept.abbr}{self.term}'.format(self=self)
    
    @property
    def year(self):
        return self.first_day.year

    @property
    def season(self):
        return ['Winter','Spring','Summer','Fall'][int(self.first_day.month / 3)]
        
    def copy_instance(self):
        instance = copy.deepcopy(self)
        instance.id = None
        instance.save()

    def __unicode__(self):
        x = '{self.title}, {self.season} {self.year}'.format(self=self)
        if not self.is_active:
            x += ' [Inactive]'
        return x

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


