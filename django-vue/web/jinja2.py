from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse


def get_excerpt(input_str, max_len=50):
    if len(input_str) <= max_len:
        return input_str

    return input_str[:max_len-3] + '...'


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'excerpt': get_excerpt
    })
    return env
