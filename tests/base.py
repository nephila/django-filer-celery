# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from celery import current_app
from django.conf import settings
from djangocms_helper.base_test import BaseTestCase

try:
    from cmsplugin_filer_image.models import ThumbnailOption
except ImportError:
    from filer.models import ThumbnailOption


class BaseFilerCelery(BaseTestCase):
    options_list = (
        {
            'size': '100x200'.split('x'),
            'crop': True,
            'HIGH_RESOLUTION': True,
        },
        {
            'size': '100x0'.split('x'),
            'crop': False,
        },
        {
            'size': '100x0'.split('x'),
            'crop': False,
            'quality': 40,
        },
    )

    def setUp(self):
        super(BaseFilerCelery, self).setUp()
        settings.CELERY_ALWAYS_EAGER = True
        current_app.conf.CELERY_ALWAYS_EAGER = True

    def create_thumbnail_options(self):
        th_options = {}
        for index, opt in enumerate(self.options_list):
            th_options[index] = ThumbnailOption.objects.create(
                name=index,
                width=opt['size'][0], height=opt['size'][1],
                crop=opt.get('crop', True)
            )
        return th_options
