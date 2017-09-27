from django.conf.urls import url

from pages import views

urlpatterns = [
    # Display all profile
    url(r'^$', views.profile_list, name='pages_profile_list'),

    # Display a single profile, given its user id
    url(r'^show/(?P<user_id>[0-9]+)/$', views.profile_show, name='pages_profile_show'),

    # Display the edit profile and user data page and send its data to profile_update page
    url(r'^edit/(?P<user_id>[0-9]+)/$', views.profile_edit, name='pages_profile_edit'),

    # Do not display a page, just get the data from profile_edit, updates and redirect to edit page
    url(r'^update/(?P<user_id>[0-9]+)/$', views.profile_update, name='pages_profile_update'),

    # Display a loggin page
    url(r'^login/$', views.profile_login, name='pages_profile_login'),

    # Do not display a page, just remove the current user from the session and redirect to loggin page
    url(r'^logout/$', views.profile_logout, name='pages_profile_logout'),

    # Display a register form for a new user
    url(r'^signup/$', views.profile_signup, name='pages_profile_signup'),

    # Do not display a page, just register the new user and redirect it to the loggin page
    url(r'^register/$', views.profile_register, name='pages_profile_register'),
]