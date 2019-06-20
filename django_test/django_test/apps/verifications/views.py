from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response

from . import constants
from django_test.libs.captcha.captcha import captcha
# Create your views here.

import logging
logger = logging.getLogger('django')


class GetImageCodeView(APIView):
    """
    图片验证码
    """
    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()

        redis_conn = get_redis_connection("verify_codes")

        redis_conn.set("img_%s" % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

        response = HttpResponse(image, content_type='image/jpg')
        response['text'] = text
        logger.info(text)
        return response


class VerifyImageCodeView(APIView):
    """
    验证图片
    """
    def post(self, request):
        data = request.data
        image_code_id = data['image_code_id']
        image_code_text = data['image_code_text']

        redis_conn = get_redis_connection("verify_codes")
        try:
            image_server_code = redis_conn.get('img_%s' % image_code_id)
        except Exception as e:
            raise serializers.ValidationError('请重试')
        if image_server_code is None:
            raise serializers.ValidationError('验证码过期')
        if image_server_code.decode() == image_code_text.upper():
            return Response({'massage': 'OK'})
        else:
            return Response({'massage': '验证码错误'})