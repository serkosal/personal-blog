from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(req: HttpRequest) -> HttpResponse:
    
    return render(req, "main/index.html", {"title": "Main page"})


def attributions(req: HttpRequest):
    
    return render(req, "main/attributions.html", {"attributions": "attributions"})