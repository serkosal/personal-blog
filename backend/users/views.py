from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse

# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "registration/register.html"


def profile(req: HttpRequest) -> HttpResponse:

    return render(req, "registration/profile.html", {"title": "homepage"}) 