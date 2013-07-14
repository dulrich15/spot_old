from __future__ import division
from __future__ import unicode_literals

import os
import shutil

from django.contrib import messages
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
def build_document(request, classroom_pk, activity_pk, docmaker_pk):
    context = {}

    classroom = Classroom.objects.get(pk=classroom_pk)
    context['classroom'] = classroom

    docmaker = Docmaker.objects.get(pk=docmaker_pk)
    template = docmaker.template

    if activity_pk:
        activity = Activity.objects.get(pk=activity_pk)
        context['activity'] = activity
        context['activity_block'] = activity.activityblock_set.all()[0] ## really??? more than one activity_block per activity?
#         context['activity_block'] = activity.activityblock

        if docmaker.activity_type != activity.activity_type: # this shouldn't ever happen...
            redirect('show_classroom', classroom_pk)

        for model in context_builders.models:
            try:
                builder = model.objects.get(activity=activity)
                context.update(builder.extra_context)
                builder_tag = '{:0>2}'.builder.pk
            except:
                builder_tag = ''

    c = RequestContext(request, context)
    t = loader.get_template(template)

    latex = t.render(c)
    pdfpath = make_pdf(latex)

    filename = '{}{}{}.pdf'.format(classroom.tag, docmaker.tag, builder_tag)
    docpath = os.path.join(Document.document_path, filename)
    shutil.move(pdfpath, docpath) # this will overwrite

#     messages.info(request, 'Just created {}'.format(docpath))
#     return redirect('list_docmakers', classroom_pk)

    f = open(docpath, 'rb')
    response = HttpResponse(f.read(), mimetype='application/pdf')
    response['Content-disposition'] = 'filename=filename'
#     response['Content-disposition'] = 'attachment; filename=filename'

    return response

