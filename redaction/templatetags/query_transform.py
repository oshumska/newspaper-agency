from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for name, value in kwargs.items():
        if value is not None:
            updated[name] = value
        else:
            updated.pop(name, 0)
    return updated.urlencode()
