from . import views
from django.urls import path, re_path


urlpatterns = [
    path('image/code/<int:image_code_id>/', views.GetImageCodeView.as_view()),
    path('image/code/', views.VerifyImageCodeView.as_view()),
]
