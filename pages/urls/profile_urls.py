from django.conf.urls import url

from pages import views

urlpatterns = [
    url(r'^$', views.profile_list, name='pages_profile_list'),
]
