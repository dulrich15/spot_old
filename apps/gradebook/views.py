from __future__ import division
from __future__ import unicode_literals

from mimetypes import guess_type

from django.contrib import messages
from django.http import HttpResponse
from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.shortcuts import redirect
from django.views.static import serve

from decorators import *
from models import *


def list_assignments(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'gradebook/list_assignments.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


# def show_classroom(request, classroom_pk):
#     classroom = Classroom.objects.get(pk=classroom_pk)
#     context = {
#         'classroom': classroom,
#     }
#     template = 'classroom/show_classroom.html'
#
#     c = RequestContext(request, context)
#     t = loader.get_template(template)
#
#     return HttpResponse(t.render(c))


# @verify_user_is_staff(redirect_url_name='show_classroom')
# def edit_classroom(request, classroom_pk):
    # classroom = Classroom.objects.get(pk=classroom_pk)
    # context = {
        # 'classroom': classroom,
    # }
    # template = 'classroom/edit_classroom.html'

    # c = RequestContext(request, context)
    # t = loader.get_template(template)

    # return HttpResponse(t.render(c))


