# custom_filters.py
from django import template

register = template.Library()


@register.filter
def multiply_and_divide(value, arg):
    return (value * arg) / 100
