from django import template
from django.utils.safestring import mark_safe

import docutils

register = template.Library()

@register.filter(is_safe=True)
def rst2html(source, overrides={}):
    '''Wrapper for docutils ``publish_parts`` HTML writer.'''
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
        html = docutils.core.publish_parts(
            source=source,
            writer_name=writer,
            settings_overrides=settings_overrides,
        )['body']
        html = html.replace('---','&mdash;')
        html = html.replace('--','&ndash;')
        html = html.replace('...','&hellip;')
    else:
        html = ''
        
    return mark_safe(html.strip())

