from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'api/profile/$', views.ProfileList.as_view()),
    url(r'api/profile/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view()),
]
