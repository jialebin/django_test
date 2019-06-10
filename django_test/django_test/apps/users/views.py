from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView


from .serializers import CreateUserSerializer


def hello(request):
    return HttpResponse('Hello world')


class CreateUser(CreateAPIView):

    serializer_class = CreateUserSerializer
