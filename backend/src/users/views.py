from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404

from .models import Profile
from .forms import ProfileChangeForm
from .serializers import UserSerializer

# Create your views here.

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "registration/register.html"


def profile(req: HttpRequest) -> HttpResponse:
    
    context = {"title": "homepage", "render_user": req.user}
    
    if hasattr(req.user, 'profile') and req.user.profile:
        profile: Profile = req.user.profile
        
        context["can_edit"] = profile.can_edit(req.user)
    
    return render(req, "registration/profile.html", context)


class ProfileUpdate(UpdateView):
    form_class = ProfileChangeForm
    template_name = 'users/profileUpdate.html'
    
    def get_object(self, queryset = None):
        user_id: int = self.kwargs["user_id"]
        
        User = get_user_model()
        
        user = get_object_or_404(User, pk=user_id)
        profile: Profile = user.profile
        
        if profile.can_edit(self.request.user):
            return profile
        else:
            raise Http404
    
    
    def form_valid(self, form: ProfileChangeForm):
        profile: Profile = form.instance
        user = self.request.user
        
        return profile.can_edit(user) and super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy("users:profile")


def detail(req: HttpRequest, user_id: int) -> HttpResponse:

    user_model = get_user_model()
    
    other_user = get_object_or_404(user_model, pk=user_id)
    
    if not hasattr(other_user, 'profile'):
        raise Http404
    
    profile: Profile = other_user.profile

    if not profile.can_see(req.user):
        raise Http404

    context = {
        "title": "homepage", 
        "render_user": other_user,
        "can_edit": profile.can_edit(req.user)
    }

    return render(req, "registration/profile.html", context)


def api_detail(req: HttpRequest, user_id: int) -> HttpResponse:
    
    user_model = get_user_model()
    
    try:
        user = user_model.objects.get(pk=user_id)
    except user_model.DoesNotExist:
        return JsonResponse({"error": "Requested user does not exist!"} , status=404)
    
    user_json = UserSerializer(user)
    
    return JsonResponse(user_json.data, status=200)