# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os.path

from easy_thumbnails.alias import aliases
from easy_thumbnails.files import get_thumbnailer

from filer_celery.models import get_thumbnail_lazy
from filer_celery.tasks import generate_thumbnail, generate_thumbnails
from filer_celery.utils import load_aliases

from .base import BaseFilerCelery


class TestFiler_celery(BaseFilerCelery):
    def test_get_thumbnail_lazy(self):
        base_image = self.create_filer_image_object()
        for opt in self.options_list:
            quality = opt.get('quality', 95)
            retval = get_thumbnail_lazy(base_image, opt)
            self.assertTrue(os.path.exists(retval.path))
            full_path = retval.path.replace('_q10_', '_q{}_'.format(quality))
            self.assertTrue(os.path.exists(full_path))
            full_path = '{}@2x.jpg'.format(full_path[:-4])
            self.assertTrue(os.path.exists(full_path))

    def test_aliases_load(self):
        th_options = self.create_thumbnail_options()

        load_aliases()
        self.assertEqual(len(aliases.all()), 3)
        for name, alias in aliases.all().items():
            index = int(name)
            self.assertEqual(self.options_list[index]['size'][0], th_options[index].width)
            self.assertEqual(self.options_list[index]['size'][1], th_options[index].height)

    def test_generate_thumbnails(self):
        base_image = self.create_filer_image_object()
        self.create_thumbnail_options()

        model = '{}.{}'.format(base_image._meta.app_label, base_image._meta.model_name)
        generate_thumbnails(model, base_image.pk, 'file')
        for alias in aliases.all():
            existing = get_thumbnailer(base_image)[alias]
            self.assertTrue(existing)
            self.assertTrue(os.path.exists(existing.path))

    def test_generate_thumbnail(self):
        base_image = self.create_filer_image_object()
        for opt in self.options_list:
            model = '{}.{}'.format(base_image._meta.app_label, base_image._meta.model_name)
            generate_thumbnail(model, base_image.pk, 'file', opt)
            existing = get_thumbnailer(base_image).get_existing_thumbnail(opt)
            self.assertTrue(existing)
            self.assertTrue(os.path.exists(existing.path))
