# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from easy_thumbnails.alias import aliases


def load_aliases():
    """
    Load ThumbnailOption as easy-thumbnails aliases
    """
    def _load_aliases():
        try:
            from cmsplugin_filer_image.models import ThumbnailOption
        except ImportError:
            from filer.models import ThumbnailOption
        thumbs = ThumbnailOption.objects.all()
        for thumb in thumbs:
            if not aliases.get(thumb.name):
                aliases.set(thumb.name, thumb.as_dict)

    try:  # pragma: no cover
        if not aliases.filer_loaded:
            _load_aliases()
    except AttributeError:  # pragma: no cover
        _load_aliases()
    aliases.filer_loaded = True
