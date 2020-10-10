#_*_coding:utf-8

from django import template
register=template.Library()

@register.filter
def kong_upper(val):
    print('val from template:',val)
    return val.upper()

from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_pag,loop_pag):
    offset = abs(curr_pag)