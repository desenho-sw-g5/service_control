from django.conf.urls import url

from pages import views

urlpatterns = [
    url(r'^$', views.profile_list, name='pages_profile_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.profile_show, name='pages_profile_show'),
    url(r'^create/$', views.profile_create, name='pages_profile_create'),
]
