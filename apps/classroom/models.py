from __future__ import division
from __future__ import unicode_literals

import copy
import datetime
import os
import posixpath

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import *

from website.utils import access_choices
from website.utils import weekday_choices
from website.utils import get_choices_from_path


class Classroom(Model):
    dept = ForeignKey('Department')
    term = CharField(max_length=200)
    first_day = DateField()

    subtitle = CharField(max_length=200, blank=True)
    instructor = ForeignKey('Instructor', null=True, blank=True)

    overview = TextField(blank=True)
    scratchpad = TextField(blank=True)

    @property
    def title(self):
        return '{self.dept} {self.term}'.format(self=self)

    @property
    def abbr(self):
        return '{self.dept.abbr}{self.term}'.format(self=self)

    @property
    def year(self):
        return self.first_day.year

    @property
    def season(self): # notice: June should be *summer* term
        return ['Winter','Spring','Summer','Fall'][int((self.first_day.month + 1)/ 3)]

    @property
    def tag(self):
        return '{self.year}{self.dept.abbr[0]}{self.term}'.format(self=self).lower()

    @property
    def documents(self):
        q = Document.objects.filter(classroom=self)
        q = q.exclude(activity__in=self.activity_set.all())
        return q

    def copy_instance(self):
        instance = copy.deepcopy(self)
        instance.id = None
        instance.save()

    def __unicode__(self):
        return '{self.title}, {self.season} {self.year}'.format(self=self)

    class Meta:
        ordering = ['-first_day']


class Department(Model):
    name = CharField(max_length=200, blank=True)
    abbr = CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


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


class Student(Model):
    classroom = ForeignKey(Classroom)
    user = ForeignKey(User)

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def full_name(self):
        return '{self.last_name}, {self.first_name}'.format(self=self)

    def __unicode__(self):
        return '{self.full_name} in {self.classroom}'.format(self=self)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class Document(Model):
    classroom = ForeignKey('Classroom')
    filename = CharField(max_length=200, choices=get_choices_from_path(settings.DOCUMENT_PATH))
    label = CharField(max_length=200, null=True, blank=True)
    access_index = PositiveSmallIntegerField(choices=access_choices, verbose_name='access', default=0)

    @property
    def access(self):
        return access_choices[self.access_index][1]

    @property
    def filepath(self):
        return os.path.join(settings.DOCUMENT_PATH, self.filename)

    @property
    def exists(self):
        return os.path.isfile(os.path.join(settings.DOCUMENT_PATH, self.filepath))

    def delete(self):
        print 'attmpting to remove ' + self.filepath
        if self.exists:
            os.remove(self.filepath)
        super(Document, self).delete()

    def __unicode__(self):
        if self.label:
            return self.label
        else:
            return self.filename


# split below to separate schedule app?


class ActivityBlock(Model):
    classroom = ForeignKey(Classroom)
    week = PositiveSmallIntegerField(null=True, blank=True)
    weekday_index = PositiveSmallIntegerField(choices=weekday_choices, verbose_name='weekday', null=True, blank=True)
    heading = CharField(max_length=200, null=True, blank=True)
    sort_order = PositiveSmallIntegerField(null=True, blank=True)
#     activities = ManyToManyField(Activity, null=True, blank=True)

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
            return 'ID = {self.id}'.format(self=self)

    class Meta:
        ordering = ['sort_order', 'week', 'weekday_index', 'heading']


class ActivityType(Model):
    name = CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Activity(Model):
    classroom = ForeignKey(Classroom)
    activity_type = ForeignKey(ActivityType)
    activity_block = ForeignKey(ActivityBlock)
    documents = ManyToManyField(Document, null=True, blank=True)

    @property
    def date(self):
        return self.activity_block.date

    @property
    def nbr(self):
        x = self.__class__.objects.filter(classroom=self.classroom, activity_type=self.activity_type)
        x = sorted(x, key=lambda a: a.date)
        return x.index(self) + 1

    @property
    def tag(self):
        return '{:0>2}'.format(self.nbr)

    @property
    def label(self):
        return '{self.activity_type} {self.nbr}'.format(self=self)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name_plural = 'activities'


