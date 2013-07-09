from __future__ import division
from __future__ import unicode_literals

from django.contrib import messages
from django.http import HttpResponse
from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.shortcuts import redirect

from models import *
from apps.classroom.models import Classroom


def list_docmakers(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'docmaker/list_docmakers.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


