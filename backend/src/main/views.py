"""file with views for core Django app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(req: HttpRequest) -> HttpResponse:
    """Render site's index page.

    Args:
        req (HttpRequest): HTTP request from client's browser.
        
    Returns:
        HttpResponse: HTTP response to the client with rendered HTML page.

    """
    return render(req, 'main/index.html', {'title': 'Main page'})


def attributions(req: HttpRequest):
    """Render attributions page.

    Args:
        req (HttpRequest): HTTP request from client's browser.
        
    Returns:
        HttpResponse: HTTP response to the client with rendered HTML page.

    """    
    return render(
        req, 'main/attributions.html', {'attributions': 'attributions'}
    )
