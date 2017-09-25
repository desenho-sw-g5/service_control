from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

from rest_framework.authtoken.models import Token

from core.models import Profile, User


def profile_list(request: HttpRequest) -> HttpResponse:
    profiles = Profile.objects.select_related('user').all()

    context = {
        'profiles': profiles
    }

    return render(request, "profile/list.html", context)


def profile_show(request: HttpRequest, pk: int) -> HttpResponse:
    profile = get_object_or_404(Profile.objects.select_related('user'), pk=pk)

    context = {
        'profile' : profile
    }

    return render(request, "profile/show.html", context)


def profile_create(request: HttpRequest) -> HttpResponse:
    return render(request, "profile/create.html", {})


def profile_login(request: HttpRequest) -> HttpResponse:
    if not request.user.is_anonymous():
        return redirect("pages_profile_list")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("pages_profile_list")

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
        user = User(**user_data)
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
