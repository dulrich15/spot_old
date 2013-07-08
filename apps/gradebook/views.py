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

from website.decorators import *
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


def show_assignment(request, classroom_pk, assignment_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    assignment = Assignment.objects.get(pk=assignment_pk)
    context = {
        'classroom': classroom,
        'assignment': assignment,
    }
    template = 'gradebook/show_assignment.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


def show_grades(request, classroom_pk):
    if request.user.is_staff:
        return show_student_list(request, classroom_pk)
    elif request.user.is_active:
        return show_student(request, classroom_pk)
    else:
        return redirect('show_classroom', classroom_pk)


@verify_user_is_active(redirect_url_name='show_classroom')
def show_student(request, classroom_pk, student_pk=None):
    classroom = Classroom.objects.get(pk=classroom_pk)
    if not student_pk:
        user = request.user
        student = Student.objects.get(user=user, classroom=classroom)
    else:
        student = Student.objects.get(pk=student_pk)

    context = {
        'classroom': classroom,
        'student': student,
    }
    template = 'gradebook/show_student.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


@verify_user_is_staff(redirect_url_name='show_classroom')
def show_student_list(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'gradebook/show_student_list.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))
    
    
@verify_user_is_staff(redirect_url_name='show_classroom')
def edit_grades(request, classroom_pk, assignment_pk=None):
    classroom = Classroom.objects.get(pk=classroom_pk)
    assignments = Assignment.objects.filter(classroom=classroom)
    
    if assignment_pk:
        assignment = assignments.get(pk=assignment_pk)
    else:
        assignment = assignments[0]
        
    context = {
        'classroom': classroom,
        'assignment': assignment
    }
    template = 'gradebook/edit_grades.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))
    
    
@verify_user_is_staff(redirect_url_name='show_classroom')
def post_grades(request, classroom_pk, assignment_pk=None):
    return redirect('show_classroom', classroom_pk)