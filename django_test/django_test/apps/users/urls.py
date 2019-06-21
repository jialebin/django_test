from . import views
from django.urls import path, re_path


urlpatterns = [
    path('hello/', views.hello),
    path('create/', views.CreateUser.as_view()),
    path('login/by/email/', views.LogInByEmaiiew.as_view()),
    path('activation/user/email/', views.ActivationUserByEmailView.as_view()),
    re_path(r'^count/username/(?P<username>\w+)/$', views.CountUserName.as_view()),
    re_path(r'^count/mobile/(?P<mobile>1[3-9]\d{9})/$', views.CountUserMobile.as_view()),
    re_path(r'^login/send_email/(?P<email>[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+)/$', views.LogInSendEmailView.as_view())
]
