from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def profile_list(request: HttpRequest) -> HttpResponse:
    return render(request, "profile/list.html", {})
