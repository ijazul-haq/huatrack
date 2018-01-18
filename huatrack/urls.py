from django.contrib import admin
from django.conf.urls import url, include
from website import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^website/', include('website.urls')),
    url(r'^log_out/$', views.log_out, name='log_out'),
    url(r'^admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
