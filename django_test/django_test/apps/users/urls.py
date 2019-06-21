from . import views
from django.urls import path, re_path


urlpatterns = [
    path('hello/', views.hello),
    # 注册
    path('create/', views.CreateUser.as_view()),
    # 通过邮箱验证登录
    path('login/by/email/', views.LogInByEmaiiew.as_view()),
    # 邮箱激活接口
    path('activation/user/email/', views.ActivationUserByEmailView.as_view()),
    # 查询用户名数量
    re_path(r'^count/username/(?P<username>\w+)/$', views.CountUserName.as_view()),
    # 查询手机号数量
    re_path(r'^count/mobile/(?P<mobile>1[3-9]\d{9})/$', views.CountUserMobile.as_view()),
    # 邮箱登录发送邮件验证码
    re_path(r'^login/send_email/(?P<email>[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+)/$', views.LogInSendEmailView.as_view())
]
