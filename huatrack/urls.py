from django.contrib import admin
from django.conf.urls import url, include
from website import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^website/', include('website.urls')),
    url(r'^admin/', admin.site.urls),
]
