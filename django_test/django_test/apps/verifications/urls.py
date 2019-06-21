from . import views
from django.urls import path, re_path


urlpatterns = [
    # 生成图片验证码
    path('image/code/<int:image_code_id>/', views.GetImageCodeView.as_view()),
    # 验证图片验证码
    path('image/code/', views.VerifyImageCodeView.as_view()),
    # 发送短信验证码
    re_path(r'^send/sms/(?P<mobile>1[3-9]\d{9})/$', views.SendVerifySMSView.as_view())
]
