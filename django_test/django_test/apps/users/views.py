from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
import random
import string
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from .serializers import CreateUserSerializer, LogInByEmailSerializer
from .models import User
from celery_tasks.emali.tasks import send_verify_email
from . import constants
# from django_test.libs.captcha.captcha import captcha

import logging
logger = logging.getLogger('django')


def hello(request):
    return HttpResponse('Hello world')


class CreateUser(CreateAPIView):
    """
    注册用户
    """
    serializer_class = CreateUserSerializer


class CountUserName(APIView):
    """
    查询username数量
    """
    def get(self, request, username=None):
        count = User.objects.filter(username=username).count()
        return Response({'count': count})
        pass
    pass


class CountUserMobile(APIView):
    """
    查询注册手机数量
    """
    def get(self, request, mobile=None):
        count = User.objects.filter(mobile=mobile).count()
        return Response({'count': count})
        pass
    pass


class LogInSendEmailView(APIView):
    """
    邮箱登录
    """
    def get(self, request, email):
        """
        发送登录的验证邮件
        :param request:
        :return:
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'massage': '该邮箱不存在'})
        except Exception as e:
            logger.info(e)
            return Response({'massage': '该邮箱不存在'})
        verify_str = ''.join(random.sample(string.ascii_uppercase, 6))
        # text, image = captcha.generate_captcha()  # 生成带图片的
        # send_verify_email('jlb1024@163.com', image)
        # 保存到ｒｅｄｉｓ
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.set('login_email_%s' % email, verify_str, constants.IMAGE_CODE_REDIS_EXPIRES)
        send_verify_email(email, verify_str)
        return Response({'massage': 'OK'})

    pass


class LogInByEmaiiew(APIView):

    def post(self, request):
        """

        :param request:
        :return:
        """
        data = request.data
        serializer = LogInByEmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.data
        user = User.objects.get(email=valid_data['email'])
        # 获取token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

        return response
