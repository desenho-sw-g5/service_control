from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

from rest_framework.authtoken.models import Token

from core.models import Profile, User

import logging

logger = logging.getLogger('django_test')

def profile_list(request: HttpRequest) -> HttpResponse:
    profiles = Profile.objects.select_related('user').all()

    context = {
        'profiles': profiles
    }

    return render(request, "profile/list.html", context)


def profile_show(request: HttpRequest, user_id: int) -> HttpResponse:
    profile = get_object_or_404(User.objects.select_related('profile'), pk=user_id).profile

    context = {
        'profile' : profile
    }

    return render(request, "profile/show.html", context)


def profile_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    # TODO: Only and Admin or Manager can edit other people's
    # TODO: Only Admin and Manager can edit all members
    # TODO: Only Admin can edit all managers

    user = get_object_or_404(User.objects.select_related('profile'), pk=user_id)

    return render(request, "profile/edit.html", {
        'user': user,
        'profile': user.profile
    })


def profile_update(request: HttpRequest, user_id: int) -> HttpResponse:
    # TODO: The same as the profile_edit todos

    if request.method == "POST":
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        password_changed = False # Django dont like when a user change its password

        user = get_object_or_404(User.objects.select_related('profile'), pk=user_id)

        # TODO: The must be a better way of doing this...
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password != "":
            user.set_password(password)
            password_changed = True

        try:
            user.full_clean()
            user.save()

            if password_changed:
                # For some reason, Django goes crazy when the user changes password
                # and dont re-log in the system
                logout(request)
                login(request, user)

        except ValidationError as validation_errors:
            context = {
                'user': user,
                'profile': user.profile
            }

            for key, value in dict(validation_errors).items():
                context['{}_errors'.format(key)] = value

            return render(request, "profile/edit.html", context)


    return redirect("pages_profile_edit", user_id=user.id)


def profile_login(request: HttpRequest) -> HttpResponse:
    if not request.user.is_anonymous():
        logger.debug("PROFILE VIEWS -> login, user is authenticated redirecting to profile list")
        return redirect("pages_profile_list")

    if request.method == "POST":
        logger.debug("PROFILE VIEWS -> login, method POST, loggin user")
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            logger.debug("PROFILE VIEWS -> login, user success logged, redirecting to profile list")
            login(request, user)
            return redirect("pages_profile_list")
        else:
            logger.debug("PROFILE VIEWS -> login, could not authenticate user\nusername: {}\npassword: {}".format(username, password))
            logout(request)

    return render(request, "profile/login.html", {})


def profile_logout(request: HttpRequest) -> HttpResponse:
    logout(request)

    return redirect("pages_profile_login")


def profile_signup(request: HttpRequest) -> HttpResponse:
    return render(request, "profile/signup.html", {})


def profile_register(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect("pages_profile_login")

    user_data = {
        'username': request.POST['username'],
        'password': request.POST['password'],
    }

    try:
        user = User(username=user_data['username'])
        user.set_password(user_data['password'])
        user.full_clean()
        user.save()

        Token.objects.create(user=user)

        profile = Profile(user=user)
        profile.full_clean()
        profile.save()

        login(request, user)

        return redirect("pages_profile_list")
    except ValidationError as validation_errors:
        # This errors is a workaround becouse django and jinja2 does not allow
        # a simple thing like "for err in errors['username']" in its template system...
        # shame on you django, shame on you.
        errors = {}

        for key, value in dict(validation_errors).items():
            errors['{}_errors'.format(key)] = value

        return render(request, "profile/signup.html", errors)
