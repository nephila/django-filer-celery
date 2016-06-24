# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url
from django.contrib import admin
from filer.models import Clipboard

from .views import ajax_upload

try:
    from filer.admin import ClipboardAdmin as ClipboardAdminFiler, views
except ImportError:
    from filer.admin import ClipboardAdmin as ClipboardAdminFiler
    from filer import views


admin.site.unregister(Clipboard)


@admin.register(Clipboard)
class ClipboardAdmin(ClipboardAdminFiler):
    def get_urls(self):
        return [
                   url(r'^operations/paste_clipboard_to_folder/$',
                       self.admin_site.admin_view(views.paste_clipboard_to_folder),
                       name='filer-paste_clipboard_to_folder'),
                   url(r'^operations/discard_clipboard/$',
                       self.admin_site.admin_view(views.discard_clipboard),
                       name='filer-discard_clipboard'),
                   url(r'^operations/delete_clipboard/$',
                       self.admin_site.admin_view(views.delete_clipboard),
                       name='filer-delete_clipboard'),
                   url(r'^operations/upload/(?P<folder_id>[0-9]+)/$',
                       ajax_upload,
                       name='filer-ajax_upload'),
                   url(r'^operations/upload/no_folder/$',
                       ajax_upload,
                       name='filer-ajax_upload'),
               ] + super(ClipboardAdminFiler, self).get_urls()
