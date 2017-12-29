from django.urls import re_path
from user import views

urlpatterns = [
    re_path('^$', views.index, name='index'),
]
