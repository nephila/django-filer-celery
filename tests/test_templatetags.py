# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os.path

from django.template import engines
from easy_thumbnails.files import get_thumbnailer

from .base import BaseFilerCelery


class TestFiler_celery(BaseFilerCelery):
    def test_get_thumbnail_lazy(self):
        self.create_thumbnail_options()

        base_image = self.create_filer_image_object()
        context = {
            'image': base_image
        }
        request = self.get_request(page=None, lang='en', path='/')
        template = (
            '{% load filer_celery %}\n'
            '{% generate_thumbnail image size="20x20" '
            'crop=True subject_location=image.subject_location as image_big %}\n'
            '{% generate_thumbnail image size="100x20" '
            'crop=False subject_location=image.subject_location %}\n'
            '{% generate_thumbnail image alias="1" '
            'subject_location=image.subject_location%}\n'
            '-{{ image_big.url }}-'
        )
        template_obj = engines['django'].from_string(template)
        output_first_pass = template_obj.render(context, request)
        output_second_pass = template_obj.render(context, request)
        opts = (
            {'size': (20, 20), 'crop': True},
            {'size': (100, 20), 'crop': False},
        )
        self.assertFalse(output_first_pass == output_second_pass)
        for opt in opts:
            existing = get_thumbnailer(base_image).get_existing_thumbnail(opt)
            self.assertTrue(existing)
            self.assertTrue(os.path.exists(existing.path))
            self.assertTrue(output_second_pass.find(existing.url) > -1)

            opt['quality'] = 10
            existing = get_thumbnailer(base_image).get_existing_thumbnail(opt)
            self.assertTrue(existing)
            self.assertTrue(os.path.exists(existing.path))
            self.assertTrue(output_first_pass.find(existing.url) > -1)
