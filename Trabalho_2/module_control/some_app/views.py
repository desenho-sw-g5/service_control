from django.shortcuts import render

from modules.models import ModuleControl

def home(request):
    return render(request, "home.html", {})