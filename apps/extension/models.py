from __future__ import division
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db.models import *

from website.utils import access_choices
from website.utils import get_choices_from_path

from apps.classroom.models import Classroom


class Extension(Model):
    classroom = OneToOneField(Classroom)
    banner_filename = CharField(max_length=200, choices=get_choices_from_path(settings.BANNER_PATH), null=True, blank=True)

    crn_list = CharField(max_length=200, blank=True)

    address = CharField(max_length=200, blank=True)
    room = CharField(max_length=200, blank=True)
    meeting_time = CharField(max_length=200, blank=True)
    meeting_notes = TextField(blank=True)

    textbook = ForeignKey('Textbook', null=True, blank=True)
    chapters = CharField(max_length=200, blank=True)

    topic_list_main = CharField(max_length=200, null=True, blank=True)
    topic_list_also = CharField(max_length=200, null=True, blank=True)

    outcomes = TextField(blank=True)
    outline = TextField(blank=True)

    @property
    def banner(self):
        banner = {}
        banner['name'] = self.banner_filename
        banner['path'] = os.path.join(settings.BANNER_PATH, banner['name'])
        banner['exists'] = os.path.isfile(banner['path'])
        banner['url'] = '/'.join([settings.BANNER_URL, banner['name']]).replace('//','/')
        return banner

    @property
    def crns(self):
        return [x.strip() for x in self.crn_list.split(',')]

    @property
    def topics(self):
        return {
            'main': [x.strip() for x in self.topics_list_main.split(',')],
            'also': [x.strip() for x in self.topics_list_also.split(',')],
        }

    def __unicode__(self):
        return '{self.classroom}'.format(self=self)


class Textbook(Model):
    title = CharField(max_length=200)
    author = CharField(max_length=200)
    edition = PositiveSmallIntegerField(null=True, blank=True)

    def full_title(self):
        if self.edition:
            ordinals = ['th','st','nd','rd'] + 6 * ['th']
            ed = '{}{}'.format(self.edition, ordinals[self.edition % 10])
            return '{0} ({1} edition)'.format(self.title, ed)
        else:
            return self.title

    def __unicode__(self):
        return '{0} by {1}'.format(self.full_title(), self.author)

    class Meta:
        ordering = ['author', 'title', '-edition']


class WebpageComponent(Model):
    classroom = ForeignKey(Classroom)
    title = CharField(max_length=200)
    text = TextField(blank=True)
    access_index = PositiveSmallIntegerField(choices=access_choices, verbose_name='access', default=0)

    @property
    def access(self):
        return access_choices[self.access_index][1]

    @property
    def html(self):
        context = {'classroom': classroom, 'settings': settings}
        template = self.text.encode('utf8')
        c = Context(context)
        t = Template(template)
        return rst2html(t.render(c))

    def __unicode__(self):
        return '{self.title} in {self.classroom}'.format(self=self)
