# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from copy import deepcopy

from django.conf import settings
from django.dispatch import receiver
from django.utils.six import iteritems
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.signals import saved_file, thumbnail_created
from filer import settings as filer_settings
from filer.models.abstract import BaseImage, logger

from .tasks import generate_thumbnail_from_file, generate_thumbnails


@receiver(saved_file)
def generate_thumbnails_async(sender, fieldfile, **kwargs):
    if getattr(settings, 'FILER_USE_CELERY', True):
        model = '{}.{}'.format(sender._meta.app_label, sender._meta.model_name)
        generate_thumbnails.apply_async((model, fieldfile.instance.pk, fieldfile.field.name))


def get_thumbnail_lazy(source, opts):
    try:
        thumbnailer = get_thumbnailer(source)
        generate_thumbnail_from_file.apply_async((thumbnailer, opts))
        low_opts = deepcopy(opts)
        low_opts['quality'] = 10
        thumb = thumbnailer.get_thumbnail(low_opts)
        return thumb
    except Exception as e:  # pragma: no cover
        if filer_settings.FILER_ENABLE_LOGGING:
            logger.error('Error while generating thumbnail: %s', e)
        if filer_settings.FILER_DEBUG:
            raise


def _generate_thumbnails(self, required_thumbnails):
    _thumbnails = {}
    for name, opts in iteritems(required_thumbnails):
        try:
            opts.update({'subject_location': self.subject_location})
            thumb = get_thumbnail_lazy(self, opts)
            _thumbnails[name] = thumb.url
        except Exception as e:  # pragma: no cover
            # catch exception and manage it. We can re-raise it for debugging
            # purposes and/or just logging it, provided user configured
            # proper logging configuration
            if filer_settings.FILER_ENABLE_LOGGING:
                logger.error('Error while generating thumbnail: %s', e)
            if filer_settings.FILER_DEBUG:
                raise
    return _thumbnails

BaseImage._generate_thumbnails = _generate_thumbnails

try:
    from image_diet.signals import optimize_file, optimize_thumbnail

    from .tasks import squeeze_task

    @receiver(saved_file)
    def optimize_file_celery(sender, fieldfile, **kwargs):
        squeeze_task.apply_async((fieldfile.path,))

    @receiver(thumbnail_created)
    def optimize_thumbnail_celery(sender, **kwargs):
        squeeze_task.apply_async((sender.path,))

    saved_file.disconnect(optimize_file)
    thumbnail_created.disconnect(optimize_thumbnail)
except ImportError:
    pass
