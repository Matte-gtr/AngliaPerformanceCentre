from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    req = context['request'].GET.copy()
    for key, value in kwargs.items():
        req[key] = value
    for key in [key for key, value in req.items() if not value]:
        del req[key]
    return req.urlencode()
