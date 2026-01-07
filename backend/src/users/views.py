from celery.result import AsyncResult 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404

from .models import Profile, Follow
from .forms import ProfileChangeForm
from .tasks import process_avatar

# Create your views here.
    

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "registration/register.html"


def profile(req: HttpRequest) -> HttpResponse:
    
    context = {"title": "homepage", "render_user": req.user}
    
    if hasattr(req.user, 'profile') and req.user.profile:
        profile: Profile = req.user.profile
        
        context["can_edit"] = profile.can_be_edited(by=req.user)
        context["followers"] = profile.followers.all()
        context["following"] = profile.following.all()
    
    return render(req, "registration/profile.html", context)


class ProfileUpdate(UpdateView):
    form_class = ProfileChangeForm
    template_name = 'users/profileUpdate.html'
    
    object: Profile | None
    
    def get_object(self, queryset = None):
        user_id: int = self.kwargs["user_id"]
        
        User = get_user_model()
        
        user = get_object_or_404(User, pk=user_id)
        profile: Profile = user.profile
        
        if profile.can_be_edited(by=self.request.user):
            return profile
        else:
            raise Http404
    
    
    def form_valid(self: ProfileUpdate, form: ProfileChangeForm):
        
        response = super().form_valid(form)
        
        profile = self.object
        
        result: AsyncResult[bool] = process_avatar.delay(profile.pk)
        
        return response
    
    
    def get_success_url(self):
        return reverse_lazy("users:profile")


def detail(req: HttpRequest, user_id: int) -> HttpResponse:

    user_model = get_user_model()
    other_user = get_object_or_404(user_model, pk=user_id)
    
    other_profile: Profile = other_user.profile
    profile: Profile = req.user.profile

    if not other_profile.can_be_seen(by=req.user):
        raise Http404

    context = {
        "title": "homepage", 
        "render_user": other_user,
        "can_edit": profile.can_be_edited(req.user),
        "can_follow": req.user != other_user,
        "is_followed": other_profile.is_followed(by=profile),
        "followers": other_profile.followers.all(),
        "following": other_profile.following.all()
    }

    return render(req, "registration/profile.html", context)


@login_required
def toggle_follow(req: HttpRequest, user_id: int):
    
    user_model = get_user_model()
    user_target = get_object_or_404(user_model, pk=user_id)
    
    if (not hasattr(user_target, 'profile') 
        or not isinstance(user_target.profile, Profile)):
        raise Http404
    
    if (not hasattr(req.user, 'profile') 
        or not isinstance(req.user.profile, Profile)):
        raise Http404
    
    profile_target = user_target.profile
    profile = req.user.profile
    
    if not profile.can_be_seen(profile_target):
        raise Http404
    
    follow_rel = Follow.objects.filter(follower=profile, followee=profile_target)
    
    if follow_rel.exists():
        profile.unfollow(profile_target)
    else:
        profile.follow(profile_target)
        
    return redirect('users:detail', user_id=user_id)