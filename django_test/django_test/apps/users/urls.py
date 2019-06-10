from . import views
from django.urls import path


urlpatterns = [
    path('hello/', views.hello),
    path('create/', views.CreateUser.as_view())
]
