from __future__ import division
from django import template

register = template.Library()

@register.filter(name="pct0")
def pct0(fraction, population=1):
    try:
        fraction = float(fraction)
        return '{0:.0%}'.format(fraction/population)
    except:
        return 'err'

@register.filter(name="pct1")
def pct1(fraction, population=1):
    try:
        fraction = float(fraction)
        return '{0:.1%}'.format(fraction/population)
    except:
        return 'err'

@register.filter(name="pct2")
def pct2(fraction, population=1):
    try:
        fraction = float(fraction)
        return '{0:.2%}'.format(fraction/population)
    except:
        return 'err'

@register.filter(name="list2text")
def list2text(lst):
    return ', '.join(lst[:-1]) + ' and ' + lst[-1]
