from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'api/person/$', views.PersonList.as_view()),
    url(r'api/person/(?P<pk>[0-9]+)/$', views.PersonDetail.as_view()),
]
