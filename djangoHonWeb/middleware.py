# middleware.py

from django.conf import settings
from django.http import HttpResponse
import mimetypes


class SetStaticMIMETypesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 检查是否是静态文件请求
        if response.has_header('Content-Disposition') and response['Content-Disposition'].startswith('inline'):
            file_path = response['Content-Disposition'].split('"')[1]
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                response['Content-Type'] = mime_type

        return response
