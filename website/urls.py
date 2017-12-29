from django.conf.urls import url
from website import views

app_name = 'website'

urlpatterns = [
    url(r'^gallery/$', views.gallery, name='gallery'),
]

