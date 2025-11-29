from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def profile(req: HttpRequest) -> HttpResponse:

    return render(req, "registration/profile.html", {"title": "homepage"}) 