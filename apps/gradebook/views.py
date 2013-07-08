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
def show_student_grades(request, classroom_pk, student_pk=None):
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
    template = 'gradebook/show_student_grades.html'

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
    if 'assignment_pk' in request.POST:
        return redirect('grade_edit', classroom_pk, request.POST['assignment_pk'])

    classroom = Classroom.objects.get(pk=classroom_pk)
    try:
        assignment = Assignment.objects.get(pk=assignment_pk)
    except:
        try:
            assignment = Assignment.objects.filter(classroom=classroom)[0]
        except:
            assignment = None

    context = {
        'classroom': classroom,
        'assignment': assignment,
    }
    template = 'gradebook/edit_grades.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


@verify_user_is_staff(redirect_url_name='show_classroom')
def post_grades(request, classroom_pk, assignment_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    assignment = Assignment.objects.get(pk=assignment_pk)

    try:
        pts = request.POST['max_points']
        assignment.max_points = int(pts)
    except:
        assignment.max_points = 0
    try:
        pts = request.POST['curve_points']
        assignment.curve_points = int(pts)
    except:
        assignment.curve_points = 0
    assignment.is_graded = ( 'is_graded' in request.POST )
    assignment.save()
    
    for student in classroom.student_set.all():
        try:
            g = AssignmentGrade.objects.get(student=student,assignment=assignment)
        except:
            g = AssignmentGrade(student=student,assignment=assignment)

        try:
            pts = request.POST['earned_points_{}'.format(student.pk)]
            g.earned_points = int(pts)
        except:
            g.earned_points = 0
        try:
            pts = request.POST['extra_points_{}'.format(student.pk)]
            g.extra_points = int(pts)
        except:
            g.extra_points = 0
        g.is_excused = ( 'is_excused_{}'.format(student.pk) in request.POST )
        g.save()
        
    messages.info(request, "Grades have been updated.")
    return redirect('grade_edit', classroom_pk, assignment_pk)