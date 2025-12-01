from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, JsonResponse


from .serializers import UserSerializer

# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "registration/register.html"


def profile(req: HttpRequest) -> HttpResponse:

    return render(req, "registration/profile.html", {"title": "homepage"})


def api_detail(req: HttpRequest, profile_id: int) -> HttpResponse:
    
    user_model = get_user_model()
    
    try:
        user = user_model.objects.get(pk=profile_id)
    except user_model.DoesNotExist:
        return JsonResponse({"error": "Requested user does not exist!"} , status=404)
    
    user_json = UserSerializer(user)
    
    return JsonResponse(user_json.data, status=200)