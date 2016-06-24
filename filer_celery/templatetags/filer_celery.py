# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Options, Tag
from django.template import Library
from easy_thumbnails.alias import aliases
from easy_thumbnails.files import get_thumbnailer

from filer_celery.models import get_thumbnail_lazy

register = Library()


@register.tag
class AsyncThumbnailer(Tag):
    """
    Generates thumbnail asynchronously

    If thumbnail for given parameters exists, it's returned, if it does not exists
    generation is offloaded to celery, while a low resolution version is rendered
    synchronously.

    """
    name = 'generate_thumbnail'
    options = Options(
        Argument('source'),
        MultiKeywordArgument('options', required=False),
        Argument('async', required=False, default=True),
        'as',
        Argument('varname', required=False, resolve=False),
    )

    def render_tag(self, context, source, options, async, varname):
        if 'size' in options:
            options['size'] = options['size'].split('x')
        try:
            opts_rest = options
            options = aliases.get(options['alias'], target=None)
            options.update(opts_rest)
        except KeyError:
            pass
        existing = get_thumbnailer(source).get_existing_thumbnail(options)
        if not existing:
            existing = get_thumbnail_lazy(source, options)
        if varname:
            context[varname] = existing
            return ''
        else:
            return existing.url
