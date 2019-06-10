from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


from .serializers import CreateUserSerializer
from .models import User


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
