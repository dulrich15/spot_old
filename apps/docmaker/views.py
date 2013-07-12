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

    docmakers = []
    for docmaker in docmaker_list:
        try:
            objects = docmaker.objects.filter(activity__classroom=classroom)
        except: # for the syllabus
            objects = docmaker.objects.filter(classroom=classroom)

        docmakers.append({
            'class': docmaker,
            'label': docmaker._meta.verbose_name_plural,
            'objects': objects,
        })

    context = {
        'classroom': classroom,
        'docmakers': docmakers,
    }
    template = 'docmaker/list_docmakers.html'

    c = RequestContext(request, context)
    t = loader.get_template(template)

    return HttpResponse(t.render(c))


@verify_user_is_staff(redirect_url_name='show_classroom')
def build_document(request, classroom_pk, doctag, obj_pk):
    classroom = Classroom.objects.get(pk=classroom_pk)

    try:
        obj = None
        for docmaker in docmaker_list:
            if doctag in docmaker.doctags:
                obj = docmaker.objects.get(pk=obj_pk)
        assert obj is not None
    except:
        messages.info(request, 'No enough information to build document')
        return redirect('list_docmakers', classroom_pk)

    context, template = obj.get_document_info(doctag)

    c = RequestContext(request, context)
    t = loader.get_template(template)

    latex = t.render(c)
    pdfpath = make_pdf(latex)

    filename = '{}{}{:0>2}.pdf'.format(classroom.tag, doctag, obj_pk)
    docpath = os.path.join(Document.document_path, filename)
    shutil.move(pdfpath, docpath) # this will overwrite

#     messages.info(request, 'Just created {}'.format(docpath))
#     return redirect('list_docmakers', classroom_pk)

    f = open(docpath, 'rb')
    response = HttpResponse(f.read(), mimetype='application/pdf')
    response['Content-disposition'] = 'filename=filename'
#     response['Content-disposition'] = 'attachment; filename=filename'

    return response

