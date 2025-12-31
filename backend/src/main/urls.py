"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import index

from django.views.generic.base import TemplateView

app_name = "main"
urlpatterns = [
    path(
        "robots.txt", 
        TemplateView.as_view(
            template_name="main/robots.txt", 
            content_type="text/plain"
        )
    ),
    
    path(
        "google79b3c578f8f2f335.html", 
        TemplateView.as_view(
            template_name="main/google79b3c578f8f2f335.html", 
            content_type="text/plain"
        )
    ),
    
    path("accounts/", include("users.urls")),
    path("blog/", include("blog.urls")),
    path('', index, name="index"),
    path('admin/', admin.site.urls)
]
