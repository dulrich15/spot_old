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


def run_docmaker(request, classroom_pk, docmaker_pk):
    pass


# @app.route('/build/syllabus')
# def build_syllabus():
    # if not current_user.access == 2:
        # return redirect(url_for('index'))

    # context = { 'course': course }
    # template = 'sy.tex'
    # latex = render_template(template, **context)

    # filename = '{}sy.pdf'.format(course.id)

    # pdfpath = make_pdf(latex)
    # docpath = os.path.join(course.lib, 'docs', filename)
    # shutil.move(pdfpath, docpath) # this will overwrite

    # print 'Just created {}'.format(docpath)

    # return redirect(url_for('serve_document', filename='syllabus'))


# @app.route('/build')
# def build_all():
    # if not current_user.access == 2:
        # return redirect(url_for('index'))

    # build_syllabus()
    # documents = Document.documents
    # for filename in documents.keys():
        # docmaker(filename)
    # return redirect(url_for('index'))


# @app.route('/build/<filename>')
# def build_document(filename):
    # if not current_user.access == 2:
        # return redirect(url_for('index'))

    # if docmaker(filename):
        # return redirect(url_for('index'))
    # else:
# #         flash('Built {} -- Would you like to <a href="{}">see it?</a>'.format(filename, url_for('serve_document', filename=filename)))
# #         return redirect(url_for('index'))
        # return redirect(url_for('serve_document', filename=filename))
