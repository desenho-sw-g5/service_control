from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

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
