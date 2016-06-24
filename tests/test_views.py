# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from filer.models import Folder, Image
from tests.base import BaseFilerCelery


class TestFilerCeleryViews(BaseFilerCelery):
    def test_upload(self):
        image = self.create_django_image_object()
        self.assertEqual(Image.objects.count(), 0)
        folder = Folder.objects.create(name='foo')
        with self.login_user_context(self.user):
            url = reverse('admin:filer-ajax_upload', kwargs={'folder_id': folder.pk})
            post_data = {
                'Filename': image.name,
                'Filedata': image,
                'jsessionid': self.client.session.session_key
            }
            self.client.post(url, post_data)
            self.assertEqual(Image.objects.count(), 1)
            self.assertEqual(Image.objects.all()[0].original_filename, image.name)

    def test_upload_no_folder(self):
        image = self.create_django_image_object()
        self.assertEqual(Image.objects.count(), 0)
        with self.login_user_context(self.user):
            url = reverse('admin:filer-ajax_upload', kwargs={'folder_id': 200})
            post_data = {
                'Filename': image.name,
                'Filedata': image,
                'jsessionid': self.client.session.session_key
            }
            response = self.client.post(url, post_data)
            self.assertContains(response, 'Can\'t find folder to upload')

    def test_upload_no_permission(self):
        from filer import settings
        settings.FILER_ENABLE_PERMISSIONS = True
        image = self.create_django_image_object()
        self.assertEqual(Image.objects.count(), 0)
        folder = Folder.objects.create(name='foo')
        with self.login_user_context(self.user_normal):
            url = reverse('admin:filer-ajax_upload', kwargs={'folder_id': folder.pk})
            post_data = {
                'Filename': image.name,
                'Filedata': image,
                'jsessionid': self.client.session.session_key
            }
            response = self.client.post(url, post_data)
            self.assertContains(response, 'Permission Denied')
        settings.FILER_ENABLE_PERMISSIONS = False

    def test_upload_no_form(self):
        self.assertEqual(Image.objects.count(), 0)
        folder = Folder.objects.create(name='foo')
        with self.login_user_context(self.user):
            url = reverse('admin:filer-ajax_upload', kwargs={'folder_id': folder.pk})
            post_data = {
                'jsessionid': self.client.session.session_key
            }
            response = self.client.post(url, post_data)
            self.assertEqual(response.status_code, 500)
            self.assertTrue(force_text(response.content).find('AJAX request not valid') > -1)
