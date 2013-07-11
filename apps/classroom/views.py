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


def list_classrooms(request):
    classrooms = Classroom.objects.all()
    context = {
        'classrooms': classrooms,
    }
    template = 'classroom/list_classrooms.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


def show_classroom(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'classroom/show_classroom.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


def show_schedule(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'classroom/show_schedule.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


def list_documents(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'classroom/list_documents.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


def serve_document(request, classroom_pk, filename):
    classroom = Classroom.objects.get(pk=classroom_pk)
    filepath = os.path.join(Document.document_path, filename)
    document = Document.objects.get(filepath=filepath)

    if request.user.is_staff:
        user_access_index = 2
    elif request.user.is_active:
        user_access_index = 1
    else:
        user_access_index = 0

    if user_access_index >= document.access_index:
        f = open(document.abspath, 'rb')
        response = HttpResponse(f.read(), mimetype=guess_type(document.basename)[0])
        return response
    else:
        return redirect('show_documents', classroom_pk)

        
@verify_user_is_staff(redirect_url_name='show_classroom')
def list_students(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    context = {
        'classroom': classroom,
    }
    template = 'classroom/list_students.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))
