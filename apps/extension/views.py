from __future__ import division
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import Context
from django.template import RequestContext
from django.template import loader

from website.decorators import *
from models import *


def show_classroom(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'extension/show_classroom.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))
