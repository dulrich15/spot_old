from __future__ import division
from __future__ import unicode_literals

import os
from datetime import datetime

from django.http import HttpResponse
from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.shortcuts import redirect

from decorators import *
from models import *


def list_classrooms(request):
    classrooms = Classroom.objects.all()
    context = {
        'classrooms': classrooms,
    }
    template = 'classroom/list_classrooms.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


def show_classroom(request, pk):
    classroom = Classroom.objects.get(pk=pk)
    context = {
        'classroom': classroom,
    }
    template = 'classroom/show_classroom.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


@verify_user_is_staff
def edit_classroom(request, pk):
    classroom = Classroom.objects.get(pk=pk)
    context = {
        'classroom': classroom,
    }
    template = 'classroom/edit_classroom.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))

    
@verify_user_is_staff
def post_classroom(request, pk):
    if not request.user.is_staff:
        return redirect('show_classroom', pk)
        
    return redirect('show_classroom')
    
