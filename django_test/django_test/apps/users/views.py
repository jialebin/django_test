from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
import random
import string


from .serializers import CreateUserSerializer
from .models import User
from celery_tasks.emali.tasks import send_verify_email
# from django_test.libs.captcha.captcha import captcha


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


class LogInByEmailView(APIView):
    """
    邮箱登录
    """
    def get(self, request, email):
        """
        发送登录的验证邮件
        :param request:
        :return:
        """

        verify_str = ''.join(random.sample(string.ascii_uppercase + string.digits, 6))
        # text, image = captcha.generate_captcha()  # 生成带图片的
        # send_verify_email('jlb1024@163.com', image)
        send_verify_email(email, verify_str)
        return Response({'massage': 'OK'})

    def post(self, request):
        """

        :param request:
        :return:
        """
        pass


    pass
