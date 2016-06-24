# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery.app import shared_task
from django.apps import apps
from easy_thumbnails.files import generate_all_aliases, get_thumbnailer
from filer import settings as filer_settings
from filer.models import logger


@shared_task
def generate_thumbnails(model_name, pk, field):
    from .utils import load_aliases
    load_aliases()
    model = apps.get_model(model_name)
    instance = model.objects.get(pk=pk)
    fieldfile = getattr(instance, field)
    generate_all_aliases(fieldfile, include_global=True)


@shared_task
def generate_thumbnail(model_name, pk, field, opts):
    model = apps.get_model(model_name)
    instance = model.objects.get(pk=pk)
    fieldfile = getattr(instance, field)
    thumbnail = get_thumbnailer(fieldfile).get_thumbnail(opts)
    return thumbnail.url


@shared_task
def generate_thumbnail_from_file(fieldfile, opts):
    try:
        thumbnail = get_thumbnailer(fieldfile).get_thumbnail(opts)
        return thumbnail
    except Exception as e:  # pragma: no cover
        if filer_settings.FILER_ENABLE_LOGGING:
            logger.error('Error while generating thumbnail: %s', e)
        if filer_settings.FILER_DEBUG:
            raise

try:  # pragma: no cover
    from image_diet.diet import squeeze

    @shared_task
    def squeeze_task(path):
        squeeze(path)
except ImportError:
    pass
