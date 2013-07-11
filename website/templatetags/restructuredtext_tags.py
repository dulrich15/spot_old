from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

import docutils_extensions

register = template.Library()

@register.filter(is_safe=True)
def rst2html(source,initial_header_level=2):
    overrides = { 'initial_header_level' : initial_header_level }
    return mark_safe(docutils_extensions.rst2html(source,overrides))

@register.filter(is_safe=True)
def rst2latex(source,initial_header_level=1):
    overrides = { 'initial_header_level' : initial_header_level }
    return mark_safe(docutils_extensions.rst2latex(source,overrides))

@register.filter(is_safe=True)
def latex_path(image):
    filename = '%s/%s' % ( settings.MEDIA_ROOT, image.name )
    return mark_safe(docutils_extensions.get_latex_path(filename))