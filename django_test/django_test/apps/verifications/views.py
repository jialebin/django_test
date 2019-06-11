from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django_redis import get_redis_connection

from . import constants
from django_test.libs.captcha import captcha
# Create your views here.


class ImageCodeView(APIView):
    """
    图片验证码
    """
    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()

        redis_conn = get_redis_connection("verify_codes")

        redis_conn.set("img_%s" % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

        response = HttpResponse(image, content_type='image/jpg')
        response['text'] = text
        return response