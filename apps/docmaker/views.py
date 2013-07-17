from __future__ import division
from __future__ import unicode_literals

import os
import shutil

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.shortcuts import redirect

from apps.classroom.models import Classroom, Document
from utils import make_pdf
from website.decorators import *

from models import *


@verify_user_is_staff(redirect_url_name='show_classroom')
def list_docmakers(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    docmakers = Docmaker.objects.all()

    context = {
        'classroom': classroom,
        'docmakers': docmakers,
    }
    template = 'docmaker/list_docmakers.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


@verify_user_is_staff(redirect_url_name='show_classroom')
def build_document(request, classroom_pk, docmaker_pk, activity_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    docmaker = Docmaker.objects.get(pk=docmaker_pk)

    activity = None
    if int(activity_pk):
        activity = Activity.objects.get(pk=activity_pk)

        if docmaker.activity_type:
            if docmaker.activity_type != activity.activity_type: # this shouldn't ever happen...
                return redirect('show_classroom', classroom_pk)

    context = {
        'classroom': classroom,
        'activity': activity,
    }

    for model in context_builders.models:
        try:
            builder = model.objects.get(activity=activity)
            context.update(builder.extra_context)
        except:
            pass

    template = docmaker.template

    c = RequestContext(request, context)
    t = loader.get_template(template)

    latex = t.render(c)
    pdfpath = make_pdf(latex)

    if activity:
        filename = '{}{}{}.pdf'.format(classroom.tag, docmaker.tag, activity.tag)
    else:
        filename = '{}{}.pdf'.format(classroom.tag, docmaker.tag)

    filepath = os.path.join(settings.DOCUMENT_ROOT, filename)
    shutil.move(pdfpath, filepath) # this will overwrite

    try:
        doc = Document.objects.get(classroom=classroom, filename=filename)
        doc.label = docmaker.label
    except:
        try:
            doc = Document.objects.get(classroom=classroom, label=docmaker.label)
            doc.filename = filename
        except:
            doc = Document()
            doc.classroom = classroom
            doc.filename = filename
            doc.label = docmaker.label
            doc.access_index = docmaker.access_index
    doc.save()

    if activity:
        activity.documents.add(doc)

    print "{} saved at {}".format(doc.label, doc.path)

    return redirect(doc.url)
#     return redirect('serve_document', classroom_pk, filename)


@verify_user_is_staff(redirect_url_name='show_classroom')
def build_all(request, classroom_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)
    docmakers = Docmaker.objects.all()
    activities = Activity.objects.filter(classroom=classroom)

    for docmaker in docmakers:
        if not docmaker.activity_type:
            build_document(request, classroom.pk, docmaker.pk, 0)
        else:
            for activity in activities:
                build_document(request, classroom.pk, docmaker.pk, activity.pk)

    messages.info(request, 'All documents built')
    return redirect('list_documents', classroom_pk)
