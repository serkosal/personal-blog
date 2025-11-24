from django.http import HttpRequest, HttpResponse


def index(req: HttpRequest) -> HttpResponse:
    return HttpResponse("index page!")