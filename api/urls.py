from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'profiles/$', views.ProfileList.as_view(), name='api_profiles_list'),
    url(r'profiles/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view(), name='api_profiles_detail'),
]
