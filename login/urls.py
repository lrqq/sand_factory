from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='user_login'),
    path('detail/', views.detail, name='detail'),
]
