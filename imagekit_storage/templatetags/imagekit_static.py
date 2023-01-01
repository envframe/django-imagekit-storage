from django import template
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage

from imagekit_storage import imagekit
from imagekit_storage.resource import ImageKitResource


register = template.Library()


@register.simple_tag(name='imagekit_static', takes_context=True)
def imagekit_static(context, static, options_dict=None, **options):
    if options_dict is None:
        options_dict = {}
    options = dict(options_dict, **options)

    try:
        if context['request'].is_secure() and 'secure' not in options:
            options['secure'] = True
    except KeyError:
        pass
    if not isinstance(static, ImageKitResource):
        static = staticfiles_storage.stored_name(static)
        static = imagekit.url({
            "path": static,
            "transformation": [options],
            "transformation_position": "query"
        })
    return mark_safe(static)
