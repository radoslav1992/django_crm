from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """Convert markdown text to HTML"""
    return mark_safe(md.markdown(
        text,
        extensions=[
            'extra',
            'nl2br',
            'sane_lists',
            'codehilite',
            'fenced_code',
        ]
    ))

