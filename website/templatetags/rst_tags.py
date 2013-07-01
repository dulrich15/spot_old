from django import template
# from django.conf import settings
from django.utils.safestring import mark_safe

# from ...utils import my_docutils

register = template.Library()

@register.filter(is_safe=True)
def rst2html(source,initial_header_level=2):
    return mark_safe(source)
    
    # overrides = { 'initial_header_level' : initial_header_level }
    # return mark_safe(my_docutils.rst2html(source,overrides))

# @register.filter(is_safe=True)
# def rst2latex(source,initial_header_level=1):
    # overrides = { 'initial_header_level' : initial_header_level }
    # return mark_safe(my_docutils.rst2latex(source,overrides))

# @register.filter(is_safe=True)
# def latex_path(image):
    # filename = '%s/%s' % ( settings.MEDIA_ROOT, image.name )
    # return mark_safe(my_docutils.get_latex_path(filename))
