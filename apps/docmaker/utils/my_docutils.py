# Filename : my_docutils.py
# Author: David Ulrich

# look here for improvements...
# http://www.arnebrodowski.de/blog/write-your-own-restructuredtext-writer.html

"""
My docutils extensions and helps.
"""

__docformat__ = 'reStructuredText'

import os, sys, codecs, shutil, hashlib, posixpath
from subprocess import Popen, PIPE
from PIL import Image

from django.conf import settings

from docutils import nodes
from docutils.parsers import rst
from docutils.core import publish_parts, publish_string

from settings import PROJECT_PATH, TEMP_PATH, IMAGE_PATH, IMAGE_URL
from local.config import TEX_PATH, GS_CMD, PYTHON_CMD

## -------------------------------------------------------------------------- ##

from docutils.writers import latex2e
# from docutils.writers.latex2e import PreambleCmds

class MyLatexWriter(latex2e.Writer):

    def __init__(self,initial_header_level=1):
        latex2e.Writer.__init__(self)
        if initial_header_level == 2:
            self.translator_class = MyLatexTranslator2
        elif initial_header_level == 1:
            self.translator_class = MyLatexTranslator1
        else:
            self.translator_class = MyLatexTranslator0

class MyLatexTranslator2(latex2e.LaTeXTranslator):
    section_level = 2

    def __init__(self, node):
        latex2e.LaTeXTranslator.__init__(self, node)
        self._section_number = self.section_level*[0]

class MyLatexTranslator1(latex2e.LaTeXTranslator):
    section_level = 1

    def __init__(self, node):
        latex2e.LaTeXTranslator.__init__(self, node)
        self._section_number = self.section_level*[0]

class MyLatexTranslator0(latex2e.LaTeXTranslator):
    section_level = 0

    def __init__(self, node):
        latex2e.LaTeXTranslator.__init__(self, node)
        self._section_number = self.section_level*[0]

## -------------------------------------------------------------------------- ##

def rst2latex(source, overrides={}):
    '''
    Wrapper for docutils ``publish_parts`` LaTeX writer.
    '''

    if source:
        if 'initial_header_level' in overrides.keys():
            writer = MyLatexWriter(overrides['initial_header_level'])
        else:
            writer = MyLatexWriter()

        settings_overrides = {}
        settings_overrides.update(overrides)
        latex = publish_parts(
            source=source,
            writer=writer,
            settings_overrides=settings_overrides,
        )['body']
        latex = latex.replace('-{}','-') # unwind this manipulation from docutils
    else:
        latex = ''

    return latex.strip()

def rst2html(source, overrides={}):
    '''
    Wrapper for docutils ``publish_parts`` HTML writer.
    '''

    if source:
        writer = 'html'
        settings_overrides = {
            'compact_lists' : True,
            'footnote_references' : 'superscript',
            'math_output' : 'MathJax',
            'stylesheet_path' : None,
            'initial_header_level' : 2,
            'doctitle_xform' : 0,
        }
        settings_overrides.update(overrides)
        html = publish_parts(
            source=source,
            writer_name=writer,
            settings_overrides=settings_overrides,
        )['body']
        html = html.replace('---','&mdash;')
        html = html.replace('--','&ndash;')
        html = html.replace('...','&hellip;')
    else:
        html = ''

    return html.strip()


def get_latex_path(filename):
    filename = filename.split(os.path.sep)
    for i in range(len(filename)):
        if ' ' in filename[i]:
            filename[i] = '"%s"' % filename[i]
    filename = '/'.join(filename)
    return filename

## -------------------------------------------------------------------------- ##

FIG_TEMPLATE = {
'default' : r'''
\begin{center}
%(figtext)s
%(caption)s
%(label)s
\end{center}
'''
,
'left' : r'''
%(figtext)s
%(caption)s
%(label)s
'''
,
'side' : r'''
\marginpar{
\vspace{%(offset)s}
\vspace{0.1in}
\centering
%(figtext)s
%(caption)s
%(label)s
}
'''
,
'sidecap' : r'''
\vspace{0.1in}
\begin{adjustwidth}{}{\adjwidth}
\begin{minipage}[c]{\picwidth}
\centering
%(figtext)s
\end{minipage}
\hfill
\begin{minipage}[c]{\capwidth}
%(caption)s
%(label)s
\end{minipage}
\end{adjustwidth}
\vspace{0.1in}
'''
,
'full' : r'''
\vspace{0.1in}
\begin{adjustwidth}{}{\adjwidth}
\centering
%(figtext)s
%(caption)s
%(label)s
\end{adjustwidth}
\vspace{0.1in}
'''
}

TBL_TEMPLATE = r'''
\renewcommand{\arraystretch}{1.5}
\renewcommand{\tabcolsep}{0.2cm}

\begin{tabular}{%(tblspec)s}
%(tbldata)s
\end{tabular}
'''

LATEX_TEMPLATE = r'''
\documentclass{article}
\pagestyle{empty}
\usepackage[active,tightpage]{preview}
\usepackage{p200}
\begin{document}
\begin{preview}
%s
\end{preview}
\end{document}
'''

MATPLOTLIB_TEMPLATE = r'''
from __future__ import division

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

# matplotlib.rcParams['xtick.direction'] = 'out'
# matplotlib.rcParams['ytick.direction'] = 'out'

%s

plt.savefig('temp.png')
'''

class fig_directive(rst.Directive):
    """
    ---------------------------
    Docutils directive: ``fig``
    ---------------------------

    Inserts a figure. Originally designed to support TikZ pictures. But one
    could pass any raw LaTeX code through.

    Example
    -------

    ::

        .. fig:: Some image here
            :image: image-filename.png
            :scale: 0.75

        .. fig:: Sample Trapezoid
            :position: side
            :label: trapezoid

            \begin{tikzpicture}
            \draw [fill=black!10] (-1,0.7) -- (1,0.7)
            -- (0.7,-0.7) -- (-0.7,-0.7) -- cycle;
            \end{tikzpicture}

    Options
    -------

    :image:     Used to insert images. Any content will be ignored. A label
                will be inserted with the image's filename.
    :scale:     Used to scale the image.
    :label:     Used for hyperlinks references. See ``fig`` role.
    :position:  Used to position figure within document. There are three
                possible values:

                :inline:    Placement within flow of text [default].
                :side:      Placement in side margin.
                :full:      Used for large figures---will not respect
                            margins but will center across the full page.

    Notes
    -----

    * Must have content. Will be wrapped by begin and end statements.
    * Argument used for figure caption (optional).
    * If the image option is used, the label defaults to image name.
    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'image'     : rst.directives.unchanged,
        'scale'     : rst.directives.unchanged,
        'label'     : rst.directives.unchanged,
        'position'  : rst.directives.unchanged,
        'offset'    : rst.directives.unchanged,
        }
    has_content = True

    def run(self):

        node_list = []

        try:
            scale = float(self.options['scale'])
        except:
            scale = 1.00

        if 'position' in self.options.keys():
            position = self.options['position']
        else:
            position = 'default'

# LaTeX writer specifics start (offset is ignored for HTML writer)

        if 'offset' in self.options.keys():
            offset = self.options['offset']
        else:
            offset = '0pt'

        if self.arguments:
            caption = rst2latex(self.arguments[0])
            caption = r'\captionof{figure}{%s}' % caption
        else:
            caption = ''

        if 'label' in self.options.keys():
            label = nodes.make_id(self.options['label'])
            label = r'\label{fig:%s}' % label
        else:
            label = ''

        if 'image' in self.options.keys():
            image = self.options['image']

            if str(image).rsplit('.',1)[1] in ['png','jpg','gif','pdf']:

                check_path = os.path.join(IMAGE_PATH, image)
                check_path = os.path.normpath(check_path)

                if not os.path.exists(check_path):
                    print 'Could not locate "%s"' % check_path

                latex_path = get_latex_path(check_path)

                figtext = r'\includegraphics[scale=%s]{%s}'
                figtext = figtext % (scale, latex_path)
                if not label:
                    label = nodes.make_id(image)
                    label = r'\label{fig:%s}' % label
            else:
                figtext = image
        else:
            figtext = '\n'.join(self.content)

        text = FIG_TEMPLATE[position] % {
            'offset'    : offset,
            'caption'   : caption,
            'label'     : label,
            'figtext'   : figtext,
            }

        node = nodes.raw(text=text, format='latex', **self.options)
        node_list += [node]

# HTML writer specifics start...

        if 'image' in self.options.keys():
            image = self.options['image']

            check_path = os.path.join(IMAGE_PATH, image)
            check_path = os.path.normpath(check_path)

            if os.path.exists(check_path):
                img_width, img_height = Image.open(check_path).size
                fig_width = int(img_width*scale*0.50)

                if 'label' in self.options.keys():
                    label = nodes.make_id(self.options['label'])
                else:
                    label = nodes.make_id(image)

                figtext = '\n'
                if 'side' in position:
                    # figtext += '<div id="fig:{0}" class="my-docutils fig {1}" style="width:{2}px;">\n'
                    figtext += '<div id="fig:{0}" class="my-docutils fig {1}">\n'
                else:
                    figtext += '<div id="fig:{0}" class="my-docutils fig {1}">\n'
                    # figtext += '<div id="fig:{0}" class="my-docutils fig {1}" style="width:{2}px;">\n'
                figtext = figtext.format(label, position, fig_width)

                html_path = os.path.join(IMAGE_URL, image)
                figtext += '<a href="{0}"><img width="{1}px" src="{0}"></a>\n'.format(html_path, fig_width)
                # figtext += '<a href="{0}"><img src="{0}"></a>\n'.format(html_path, fig_width)

                if self.arguments:
                    figtext += rst2html(self.arguments[0])

                figtext += '</div>\n'

            else:
                print 'Could not locate "%s"' % check_path
                figtext = '\n<p style="padding:0.5em;border:1px solid red">Missing image</p>\n'

        else: # try to construct the image
            # Unlike a normal image, our reference will come from the content...
            content = '\n'.join(self.content).replace('\\\\','\\')
            image_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            image_name = '%s.png' % image_hash
            image_path = os.path.join(IMAGE_PATH, 'latex', image_name)
            image_url = posixpath.normpath(os.path.join(IMAGE_URL, 'latex', image_name))
            self.options['uri'] = image_url

            try:
                # Maybe we already made it? If not, make it now...
                if not os.path.isfile(image_path):

                    print 'Making image %s' % image_name
                    print image_path
                    print image_url

                    # Set up our folders and filename variables
                    curdir = os.getcwd()

                    # Write the LaTeX file to the image folder
                    os.chdir(os.path.join(TEMP_PATH, 'latex'))
                    f = codecs.open('temp.tex', 'w', 'utf-8')
                    f.write(LATEX_TEMPLATE % content)
                    f.close()

                    # Run LaTeX ...
                    cmd = os.path.join(TEX_PATH, 'pdflatex')
                    cmd = [cmd,
                    '--interaction=nonstopmode',
                    'temp.tex'
                    ]
                    p = Popen(cmd,stdout=PIPE,stderr=PIPE)
                    out, err = p.communicate()

                    cmd = [GS_CMD,
                    '-q',
                    '-dBATCH',
                    '-dNOPAUSE',
                    '-sDEVICE=png16m',
                    '-r600',
                    '-dTextAlphaBits=4',
                    '-dGraphicsAlphaBits=4',
                    '-sOutputFile=temp.png',
                    'temp.pdf',
                    ]
                    p = Popen(cmd,stdout=PIPE,stderr=PIPE)
                    out, err = p.communicate()

                    img = Image.open('temp.png')
                    img_scale = 0.40 * scale
                    print img_scale
                    img_width = int(img_scale * img.size[0])
                    img_height = int(img_scale * img.size[1])
                    img = img.resize((img_width, img_height), Image.ANTIALIAS)
                    img.save('temp.png', 'png')

                    # Finally, move the image file and clean up

                    shutil.copyfile('temp.png', image_path)
                    # os.remove('rm temp.*')
                    os.chdir(curdir)

                self.options['alt'] = self.content

                img_width, img_height = Image.open(image_path).size
                fig_width = int(img_width*scale*0.50)

                if 'label' in self.options.keys():
                    label = nodes.make_id(self.options['label'])
                else:
                    label = nodes.make_id(image_name)

                figtext = '\n'
                # figtext += '\n<div id="fig:{0}" class="my-docutils fig {1}" style="width:{2}px;">\n'
                figtext += '\n<div id="fig:{0}" class="my-docutils fig {1}">\n'
                figtext = figtext.format(label, position, fig_width)

                figtext += '<a href="{0}"><img width="{1}px" src="{0}"></a>\n'.format(image_url, fig_width)
                # figtext += '<a href="{0}"><img src="{0}"></a>\n'.format(image_url, fig_width)

                if self.arguments:
                    figtext += rst2html(self.arguments[0])

                figtext += '</div>\n'

            except:
                print 'Could not locate "%s"' % image_path
                figtext = '\n<div style="padding:0.5em;border:1px solid red"><code>' + '<br>'.join(self.content) + '</code></div>\n'

        text = figtext

        node = nodes.raw(text=text, format='html', **self.options)
        node_list += [node]

        return node_list

rst.directives.register_directive('fig', fig_directive)

class plt_directive(rst.Directive):
    """
    ---------------------------
    Docutils directive: ``plt``
    ---------------------------

    Inserts a matplotlib plot.

    Example
    -------

    ::

        .. plt:: Some numbers
            :label: test-plot

            plt.plot([1,2,3,4], [1,4,9,16], 'ro')
            plt.axis([0, 6, 0, 20])
            plt.ylabel('some numbers')

    Options
    -------

    :scale:     Used to scale the image.
    :label:     Used for hyperlinks references. See ``plt`` role.
    :position:  Used to position figure within document. There are three
                possible values:

                :inline:    Placement within flow of text [default].
                :side:      Placement in side margin.
                :full:      Used for large figures---will not respect
                            margins but will center across the full page.

    Notes
    -----

    * Must have content. Will be wrapped by begin and end statements.
    * Argument used for figure caption (optional).
    * If the image option is used, the label defaults to image name.
    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'scale'     : rst.directives.unchanged,
        'label'     : rst.directives.unchanged,
        'position'  : rst.directives.unchanged,
        'offset'    : rst.directives.unchanged,
        }
    has_content = True

    def run(self):

        node_list = []

        # Unlike a normal image, our reference will come from the content...
        content = '\n'.join(self.content).replace('\\\\','\\')

        # Have to have some serious protection here....
        if '\nimport' in content:
            assert False

        # Define image name and location
        image_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        image_name = '%s.png' % image_hash
        image_path = os.path.join(IMAGE_PATH, 'matplotlib', image_name)
        image_url = posixpath.normpath(os.path.join(IMAGE_URL, 'matplotlib', image_name))
        self.options['uri'] = image_url

        # Maybe we already made it? If not, make it now...
        if not os.path.isfile(image_path):

            print 'Making image %s' % image_name
            print image_path
            print image_url

            # Set up our folders and filename variables
            curdir = os.getcwd()

            # Write the matplotlib file to the temp folder
            os.chdir(os.path.join(TEMP_PATH, 'matplotlib'))
            f = codecs.open('temp.py', 'w', 'utf-8')
            f.write(MATPLOTLIB_TEMPLATE % content)
            f.close()

            # Run matplotlib ...
            cmd = [PYTHON_CMD, 'temp.py']
            p = Popen(cmd,stdout=PIPE,stderr=PIPE)
            out, err = p.communicate()

            # Move the image file and clean up
            shutil.copyfile('temp.png', image_path)
            # os.remove('rm temp.*')
            os.chdir(curdir)

        try:
            scale = float(self.options['scale'])
        except:
            scale = 1.00

        if 'position' in self.options.keys():
            position = self.options['position']
        else:
            position = 'default'

        check_path = image_path

# LaTeX writer specifics start (offset is ignored for HTML writer)

        if 'offset' in self.options.keys():
            offset = self.options['offset']
        else:
            offset = '0pt'

        if self.arguments:
            caption = rst2latex(self.arguments[0])
            caption = r'\captionof{figure}{%s}' % caption
        else:
            caption = ''

        if 'label' in self.options.keys():
            label = nodes.make_id(self.options['label'])
            label = r'\label{plt:%s}' % label
        else:
            label = ''

        if os.path.exists(check_path):
            latex_path = get_latex_path(check_path)
            figtext = r'\includegraphics[scale=%s]{%s}'
            figtext = figtext % (scale*0.5, latex_path)
            if not label:
                label = nodes.make_id(image_name)
                label = r'\label{plt:%s}' % label
        else:
            print 'Could not locate "%s"' % check_path
            figtext = '\n'.join(self.content)

        text = FIG_TEMPLATE[position] % {
            'offset'    : offset,
            'caption'   : caption,
            'label'     : label,
            'figtext'   : figtext,
            }

        node = nodes.raw(text=text, format='latex', **self.options)
        node_list += [node]

# # HTML writer specifics start...

        if os.path.exists(check_path):
            img_width, img_height = Image.open(check_path).size
            fig_width = int(img_width*scale*0.75)

            if 'label' in self.options.keys():
                label = nodes.make_id(self.options['label'])
            else:
                label = nodes.make_id(image_name)

            figtext = '\n'
            if 'side' in position:
                # figtext += '<div id="plt:{0}" class="my-docutils plt {1}" style="width:{2}px;">\n'
                figtext += '<div id="plt:{0}" class="my-docutils plt {1}">\n'
            else:
                figtext += '<div id="plt:{0}" class="my-docutils plt {1}">\n'
                # figtext += '<div id="plt:{0}" class="my-docutils plt {1}" style="width:{2}px;">\n'
            figtext = figtext.format(label, position, fig_width)

            figtext += '<a href="{0}"><img width="{1}px" src="{0}"></a>\n'.format(image_url, fig_width)
            # figtext += '<a href="{0}"><img src="{0}"></a>\n'.format(image_url, fig_width)

            if self.arguments:
                figtext += rst2html(self.arguments[0])

            figtext += '</div>\n'

        else:
            print 'Could not locate "%s"' % check_path
            figtext = '\n<div style="padding:0.5em;border:1px solid red"><code>' + '<br>'.join(self.content) + '</code></div>\n'

        text = figtext

        node = nodes.raw(text=text, format='html', **self.options)
        node_list += [node]

        return node_list

rst.directives.register_directive('plt', plt_directive)

class tbl_directive(rst.Directive):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'label'     : rst.directives.unchanged,
        'position'  : rst.directives.unchanged,
        'offset'    : rst.directives.unchanged,
        'cols'      : rst.directives.unchanged,
        }
    has_content = True

    def run(self):

        self.assert_has_content()
        node_list = []

        if 'position' in self.options.keys():
            position = self.options['position']
        else:
            position = 'default'

        if 'offset' in self.options.keys():
            offset = self.options['offset']
        else:
            offset = '0pt'

        if self.arguments:
            caption = rst2latex(self.arguments[0])
            caption = r'\captionof{table}{%s}' % caption
        else:
            caption = ''

        if 'label' in self.options.keys():
            label = nodes.make_id(self.options['label'])
            label = r'\label{tbl:%s}' % label
        else:
            label = ''

        parser = rst.tableparser.SimpleTableParser() # GridTableParser()
        tbl = parser.parse(self.content)

        ncols = len(tbl[0])

        if 'cols' in self.options.keys():
            tblspec = self.options['cols']
        else:
            tblspec = ncols * 'c'

        tbldata = '\\hline\n'
        if tbl[1]:
            head = ncols * ['']

            # Truly, the following is overkill---it won't be used.
            # It's too difficult to deal with long table text in LaTeX.
            for rowdata in tbl[1]:
                for i in range(ncols):
                    cell = rst2latex(''.join(rowdata[i][3]))
                    head[i] = ' '.join([head[i], cell]).strip()

            for i in range(ncols):
                head[i] = '\\textbf{%s}' % head[i]
            tbldata += ' & '.join(head) + ' \\\\ \n'
            tbldata += '\\hline\n'
        if tbl[2]:
            for rowdata in tbl[2]:
                body = ncols * ['']
                for i in range(ncols):
                    cell = rst2latex(''.join(rowdata[i][3]))
                    body[i] = ' '.join([body[i], cell])
                tbldata += ' & '.join(body) + ' \\\\ \n'
        tbldata += '\\hline\n'

        tbltext = TBL_TEMPLATE % {
            'tblspec'   : tblspec,
            'tbldata'   : tbldata.strip(),
            }

        text = FIG_TEMPLATE[position] % {
            'offset'    : offset,
            'caption'   : caption,
            'label'     : label,
            'figtext'   : tbltext,
            }

        node = nodes.raw(text=text, format='latex', **self.options)
        node_list += [node]

# HTML writer specifics start...

        tbltext = '\n'

        if 'label' in self.options.keys():
            label = nodes.make_id(self.options['label'])
            tbltext += '<div id="tbl:{0}" class="my-docutils tbl {1}">\n'.format(label, position)
        else:
            tbltext += '<div class="my-docutils tbl {0}">\n'.format(position)

        tbltext += '<table>\n'

        if 'cols' in self.options.keys():
            tblspec = self.options['cols']
        else:
            tblspec = ncols * 'c'

        col_align = []
        for x in tblspec:
            if x == 'l':
                col_align += ['left']
            elif x == 'c':
                col_align += ['center']
            elif x == 'r':
                col_align += ['right']

        tbltext += '<tr>\n'
        if tbl[1]:
            head = ncols * ['']

            # Truly, the following is overkill---it won't be used.
            # It's too difficult to deal with long table text in LaTeX.
            for rowdata in tbl[1]:
                for i in range(ncols):
                    cell = rst2html(''.join(rowdata[i][3]))[3:-4]
                    head[i] = ' '.join([head[i], cell]).strip()

            for i in range(ncols):
                head[i] = u'<th>%s</th>\n' % head[i]
            tbltext += ''.join(head)
            tbltext += '<tr>\n'
        if tbl[2]:
            for rowdata in tbl[2]:
                body = ncols * ['']
                for i in range(ncols):
                    cell = rst2html(''.join(rowdata[i][3]))[3:-4]
                    body[i] = u'<td style="text-align:{1}">{0}</td>\n'.format(cell, col_align[i])
                tbltext += ''.join(body)
                tbltext += '</tr>\n'

        if self.arguments: # caption
            tbltext += '<caption>%s</caption>' % rst2html(self.arguments[0])

        tbltext += '</table>\n'
        tbltext += '</div>\n'

        text = tbltext

        node = nodes.raw(text=text, format='html', **self.options)
        node_list += [node]

        return node_list

rst.directives.register_directive('tbl', tbl_directive)

## -------------------------------------------------------------------------- ##

def ref_role(role, rawtext, text, lineno, inliner, options={}, content=[]):

    """
    ----------------------
    Docutils role: ``ref``
    ----------------------

    Inserts a hyperlink reference to a figure or table with a custom label.

    Example
    -------

   ::

        :ref:`image-filename.png`

    This will hyperlink to::

        .. fig:: Some image here
            :image: image-filename.png
            :scale: 0.75

    or

   ::

        :fig:`trapezoid`

    This will hyperlink to::

        .. fig:: Sample Trapezoid
            :position: side
            :label: trapezoid

            \begin{tikzpicture}
            \draw [fill=black!10] (-1,0.7) -- (1,0.7)
            -- (0.7,-0.7) -- (-0.7,-0.7) -- cycle;
            \end{tikzpicture}

    Notes
    -----

    * Works only for ``latex`` writer ... for now :)
    """

    ref = nodes.make_id(text)
    if role in ['fig', 'tbl']:
        ref = role + ':' + ref

    t = dict()

    t['latex'] = r'\hyperref[%s]{\ref*{%s}}' % (ref, ref)
    t['html']  = r'<a href="#%s">[link]</a>' % (ref,)

    node_list = [
        nodes.raw(text=t['latex'], format='latex'),
        nodes.raw(text=t['html'], format='html')
    ]

    return node_list, []

rst.roles.register_local_role('ref', ref_role)
rst.roles.register_local_role('fig', ref_role)
rst.roles.register_local_role('plt', ref_role)
rst.roles.register_local_role('tbl', ref_role)
rst.roles.register_local_role('eqn', ref_role) # don't forget to add tags to equations...

def jargon_role(role, rawtext, text, lineno, inliner, options={}, content=[]):

    """
    -------------------------
    Docutils role: ``jargon``
    -------------------------

    Creates an index entry then bolds the term in the main text.

    Example
    -------

   ::

        We use a :jargon:`vector` to capture both direction and magnitude.
        An important tool in QED is the :jargon:`Feynman diagram`.
        :jargon:`~Energy` is the ability to do work.

    Notes
    -----

    * Force a conversion to lower case in the index with a tilde ``~``.  Useful
      when the term starts a sentence.
    * Works only for ``latex`` and ``html`` writers ...
    """

    t = dict()

    if text[0] == '~':
        text = text[1:]
        t['latex'] = r'\textbf{%s}\index{%s}' % (text,text.lower())
        t['html'] = '<strong>%s</strong>' % text
    else:
        t['latex'] = r'\textbf{%s}\index{%s}' % (text,text)
        t['html'] = '<strong>%s</strong>' % text

    node_list = [
        nodes.raw(text=t['latex'], format='latex'),
        nodes.raw(text=t['html'], format='html')
    ]

    return node_list, []

rst.roles.register_local_role('jargon', jargon_role)

def sci_role(role, rawtext, text, lineno, inliner, options={}, content=[]):

    """
    ----------------------
    Docutils role: ``sci``
    ----------------------

    Displays scientific notation in the form :math:`a \times 10^{b}`.

    Example
    -------

   ::

        :sci:`4.5E+6`
        :sci:`450e-6`

    Notes
    -----

    * An abscissa of 1 is dropped: e.g., 1E10 => :math:`10^{10}`.
    * Upon error, the original text is returned.
    * Works only for ``latex`` and ``html`` writers ...
    """

    try:
        n = text.lower().split('e')
        a = float(n[0]) # just want to make sure it's a legit number
        a = n[0]        # make sure to take the abscissa as given
        b = int(n[1])   # must be an integer, this will drop the plus sign
        if a == '1':
            text = r'\(10^{%s}\)' % b
        else:
            text = r'\(%s \times 10^{%s}\)' % (a, b)
    except:
        pass

    node_list = [
        nodes.raw(text=text, format='latex'),
        nodes.raw(text=text, format='html'), # this pushes the work to MathJax
    ]

    return node_list, []

rst.roles.register_local_role('sci', sci_role)

def atm_role(role, rawtext, text, lineno, inliner, options={}, content=[]):

    """
    ----------------------
    Docutils role: ``atm``
    ----------------------

    Displays pretty atomic symbols.

    Example
    -------

    ::

        :atm:`235:92:U`

    Notes
    -----

    * Upon error, the original text is returned.
    * Works only for ``latex`` and ``html`` writers ...
    """

    try:

        (a, z, sy) = text.split(':')
        dn = len(a) - len(z)
        if dn > 0:
            text = r'\({}^{%s}_{\phantom{%s}%s}\text{%s}\)' % (a, dn, z, sy)
        elif dn < 0:
            text = r'\({}^{\phantom{%s}%s}_{%s}\text{%s}\)' % (-dn, a, z, sy)
        else:
            text = r'\({}^{%s}_{%s}\text{%s}\)' % (a, z, sy)
    except:
        pass

    node_list = [
        nodes.raw(text=text, format='latex'),
        nodes.raw(text=text, format='html'), # this pushes the work to MathJax
    ]

    return node_list, []

rst.roles.register_local_role('atm', atm_role)

