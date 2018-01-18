from django.conf.urls import url
from website import views

app_name = 'website'

urlpatterns = [
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_reg/$', views.user_reg, name='user_reg'),
    url(r'^collection/$', views.collection, name='collection'),
    url(r'^artwork_reg/$', views.artwork_reg, name='artwork_reg'),
    url(r'^artwork_detail/(?P<artwork_id>\d+)/$', views.artwork_detail, name='artwork_detail'),
    url(r'^asset_get/(?P<artwork_id>\d+)/$', views.asset_get, name='asset_get'),
    url(r'^asset_create/(?P<artwork_id>\d+)/$', views.asset_create, name='asset_create'),
    url(r'^asset_transfer/(?P<artwork_id>\d+)/$', views.asset_transfer, name='asset_transfer'),
    url(r'^profile/$', views.profile, name='profile'),
]
