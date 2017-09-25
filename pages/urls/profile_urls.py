from django.conf.urls import url

from pages import views

urlpatterns = [
    url(r'^$', views.profile_list, name='pages_profile_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.profile_show, name='pages_profile_show'),
    url(r'^create/$', views.profile_create, name='pages_profile_create'),
    url(r'^login/$', views.profile_login, name='pages_profile_login'),
    url(r'^logout/$', views.profile_logout, name='pages_profile_logout'),
    url(r'^signup/$', views.profile_signup, name='pages_profile_signup'),
    url(r'^register/$', views.profile_register, name='pages_profile_register'),
]