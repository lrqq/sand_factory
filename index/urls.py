from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('msg/', views.publishMsg, name='pubMsg'),
    path('getInfo/', views.get_info, name='getInfo'),
    path('snap/', views.snapImage, name='snap'),
    re_path(r'^(?P<path>.*\.jpg)$', views.getImage),

]
