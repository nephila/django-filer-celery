#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from tempfile import mkdtemp

HELPER_SETTINGS = dict(
    INSTALLED_APPS=[
        'filer',
        'easy_thumbnails',
    ],
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    THUMBNAIL_PROCESSORS=(
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters'
    ),
    BROKER_BACKEND='memory',
    CELERY_ALWAYS_EAGER=True,
    CELERY_IGNORE_RESULT=True,
    CELERYD_LOG_LEVEL='ERROR',
    THUMBNAIL_HIGH_RESOLUTION=True,
    THUMBNAIL_QUALITY=95,
)

try:
    import cmsplugin_filer_image  # pragma: no cover # NOQA

    HELPER_SETTINGS['INSTALLED_APPS'].append('cmsplugin_filer_image')
    HELPER_SETTINGS['INSTALLED_APPS'].append('cms')
    HELPER_SETTINGS['INSTALLED_APPS'].append('treebeard')
    HELPER_SETTINGS['INSTALLED_APPS'].append('menus')
    try:
        import cmsplugin_filer_image.migrations_django  # pragma: no cover # NOQA

        HELPER_SETTINGS['MIGRATION_MODULES'] = {
            'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django'
        }
    except ImportError:
        pass
except ImportError:
    pass


def run():
    from djangocms_helper import runner
    runner.run('filer_celery')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('filer_celery', sys.modules[__name__], use_cms=False)


if __name__ == '__main__':
    run()
