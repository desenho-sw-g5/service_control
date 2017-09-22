from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'api/profile/$', views.ProfileList.as_view(), name='api_profile_list'),
    url(r'api/profile/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view(), name='api_profile_detail'),
]
