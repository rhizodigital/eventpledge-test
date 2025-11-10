from django import template
from django.utils.safestring import mark_safe
from core.utils import get_site_settings

register = template.Library()


@register.simple_tag
def site_setting(field_name=None, default='', safe=False):
    """
    Template tag to retrieve site settings.
    Usage:
        {% site_setting as settings %}
        {{ settings.site_name }}
    Or for a specific field:
        {% site_setting "site_name" %}
    """
    settings = get_site_settings()
    value = getattr(settings, field_name, default)

    if value is None:
        return default

    if isinstance(value, (bool, int, float)):
        return value

    if safe:
        return mark_safe(str(value))

    return str(value)


@register.filter
def divide(value, arg):
    """
    Divides the value by the argument.
    Returns the result as a float for accurate CSS factor calculation.
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return None
