"""service_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

from decorator_include import decorator_include

from core.views_verifications import (
    ViewsVerificationsDecorator,
    LoginRequiredVerification,
    ModuleAccessVerification)

from core.enums import ModuleEnum

from pages.views import profile_login

urlpatterns = [
    url(r'^$', profile_login, name='home_page'),

    url(r'^admin/', admin.site.urls),

    url(r'^api-token-auth/', views.obtain_auth_token),

    url(r'api/', include('api.urls')),

    url(r'profiles/',
        decorator_include(
            ViewsVerificationsDecorator(
                module=ModuleEnum.MY_PROFILE,
                verifications=(
                    LoginRequiredVerification(), ModuleAccessVerification()),
                unless=('pages_profile_login', 'pages_profile_signup', 'pages_profile_register')
            ),
            'pages.urls.profile_urls'
        )
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
