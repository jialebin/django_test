from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework import status
import random

from . import constants
from django_test.libs.captcha.captcha import captcha
from celery_tasks.sms.tasks import send_verify_sms
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


class SendVerifySMSView(APIView):
    """
    发送短信验证码
    """
    def get(self, request, mobile):
        """
        :param request:
        :param mobile: 手机号
        :return:
        """
        redis_conn = get_redis_connection('verify_codes')
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({'massage': '频繁发送'}, status=status.HTTP_400_BAD_REQUEST)
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)
        send_verify_sms.delay(mobile, sms_code)
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()
        return Response({'massage': 'ok'})
