from __future__ import division
from __future__ import unicode_literals

from django.contrib import messages
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


@verify_user_is_staff(redirect_url_name='show_classroom')
def edit_classroom(request, pk):
    classroom = Classroom.objects.get(pk=pk)
    context = {
        'classroom': classroom,
    }
    template = 'classroom/edit_classroom.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))

    
@verify_user_is_staff(redirect_url_name='show_classroom')
def post_classroom(request, pk):
    if 'submit' in request.POST.keys():
        classroom = Classroom.objects.get(pk=pk)
        classroom.overview = request.POST['overview'].strip()
        classroom.subtitle = request.POST['subtitle'].strip()
        classroom.save()
        messages.info(request, "Classroom overview updated.")
    return redirect('show_classroom', pk)

    
def show_schedule(request, pk):
    classroom = Classroom.objects.get(pk=pk)
    blocks = ActivityBlock.objects.filter(classroom=classroom)
    
    classroom.schedule = blocks
    
    context = {
        'classroom': classroom,
    }
    template = 'classroom/show_schedule.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))
