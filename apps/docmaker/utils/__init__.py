from __future__ import division
from __future__ import unicode_literals

import codecs
import os

from subprocess import Popen, PIPE

from django.conf import settings


TEMP_PATH = os.path.join(settings.TEMP_PATH, 'latex')
TEX_PATH = settings.TEX_PATH



def make_pdf(latex):

    curdir = os.getcwd()
    os.chdir(TEMP_PATH)

    basename = 'temp'

    texname = '{}.tex'.format(basename)
    idxname = '{}.idx'.format(basename)
    pdfname = '{}.pdf'.format(basename)

    texfile = codecs.open(texname, 'w', 'utf-8')
    texfile.write(latex)
    texfile.close()

    # try:
        # for ext in ['idx','ind','ilg','aux','log','out','toc','tex','pdf','png']:
            # os.remove('{}.{}'.format(basename, ext))
    # except:
        # pass

    for i in range(1):
        cmd = os.path.join(TEX_PATH, 'pdflatex')
        cmd = [cmd, '--interaction=nonstopmode', texname]
        p = Popen(cmd,stdout=PIPE,stderr=PIPE)
        out, err = p.communicate()

    try:
        open(idxname)
        if os.path.getsize(idxname):

            cmd = os.path.join(TEX_PATH, 'makeindex')
            cmd = [cmd,  idxname]
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()

            cmd = os.path.join(TEX_PATH, 'pdflatex')
            cmd = [cmd, '--interaction=nonstopmode', texname]
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
    except:
        pass

    os.chdir(curdir)

    return os.path.join(TEMP_PATH, pdfname)
