# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json

from django.forms.models import modelform_factory
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from filer import settings as filer_settings
from filer.models import Folder, Image
from filer.utils.files import UploadException, handle_request_files_upload, handle_upload
from filer.utils.loader import load_object

from filer_celery.models import get_thumbnail_lazy

NO_FOLDER_ERROR = 'Can\'t find folder to upload. Please refresh and try again'
NO_PERMISSIONS_FOR_FOLDER = (
    'Can\'t use this folder, Permission Denied. Please select another folder.'
)


@csrf_exempt
def ajax_upload(request, folder_id=None):
    """
    Receives an upload from the uploader. Receives only one file at a time.
    """
    mimetype = 'application/json' if request.is_ajax() else 'text/html'
    content_type_key = 'content_type'
    response_params = {content_type_key: mimetype}
    folder = None

    if folder_id:
        try:
            # Get folder
            folder = Folder.objects.get(pk=folder_id)
        except Folder.DoesNotExist:
            return HttpResponse(json.dumps({'error': NO_FOLDER_ERROR}), **response_params)

    # check permissions
    if folder and not folder.has_add_children_permission(request):
        return HttpResponse(
            json.dumps({'error': NO_PERMISSIONS_FOR_FOLDER}), **response_params)
    try:
        if len(request.FILES) == 1:
            # dont check if request is ajax or not, just grab the file
            upload, filename, is_raw = handle_request_files_upload(request)
        else:
            # else process the request as usual
            upload, filename, is_raw = handle_upload(request)

        FileForm = None
        # find the file type
        for filer_class in filer_settings.FILER_FILE_MODELS:
            FileSubClass = load_object(filer_class)
            if FileSubClass.matches_file_type(filename, upload, request):
                FileForm = modelform_factory(
                    model=FileSubClass,
                    fields=('original_filename', 'owner', 'file')
                )
                break
        uploadform = FileForm({'original_filename': filename, 'owner': request.user.pk},
                              {'file': upload})
        if uploadform.is_valid():
            file_obj = uploadform.save(commit=False)
            # Enforce the FILER_IS_PUBLIC_DEFAULT
            file_obj.is_public = filer_settings.FILER_IS_PUBLIC_DEFAULT
            file_obj.folder = folder
            file_obj.save()

            # Try to generate thumbnails.
            if not file_obj.icons:
                # There is no point to continue, as we can't generate
                # thumbnails for this file. Usual reasons: bad format or
                # filename.
                file_obj.delete()
                # This would be logged in BaseImage._generate_thumbnails()
                # if FILER_ENABLE_LOGGING is on.
                return HttpResponse(
                    json.dumps({'error': 'failed to generate icons for file'}),
                    status=500, **response_params
                )
            thumbnail = None
            # Backwards compatibility: try to get specific icon size (32px)
            # first. Then try medium icon size (they are already sorted),
            # fallback to the first (smallest) configured icon.
            for size in (['32'] + filer_settings.FILER_ADMIN_ICON_SIZES[1::-1]):
                try:
                    thumbnail = file_obj.icons[size]
                    break
                except KeyError:  # pragma: no cover
                    continue

            json_response = {
                'thumbnail': thumbnail,
                'alt_text': '',
                'label': str(file_obj),
                'file_id': file_obj.pk,
            }
            # prepare preview thumbnail
            if type(file_obj) == Image:
                thumbnail_180_options = {
                    'size': (180, 180),
                    'crop': True,
                    'upscale': True,
                }
                thumbnail_180 = get_thumbnail_lazy(file_obj, thumbnail_180_options)
                json_response['thumbnail_180'] = thumbnail_180.url
                json_response['original_image'] = file_obj.url
            return HttpResponse(json.dumps(json_response), **response_params)
        else:
            form_errors = '; '.join(
                ['%s: %s' % (field, ', '.join(errors)) for field, errors in list(
                    uploadform.errors.items())]
            )
            raise UploadException('AJAX request not valid: form invalid "%s"' % (form_errors,))
    except UploadException as e:  # pragma: no cover
        return HttpResponse(json.dumps({'error': str(e)}), status=500, **response_params)
    except Exception as e:  # pragma: no cover
        return HttpResponse(json.dumps({'error': str(e)}), status=500, **response_params)
