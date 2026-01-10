"""file with views for 'users' Django app."""

# from celery.result import AsyncResult
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ProfileChangeForm
from .models import Follow, Profile
from .tasks import process_avatar

# Create your views here.


class RegisterView(CreateView):
    """Class is being responsible for user registration.
    
    Attributes:
        form_class: Django form is displayed on the page.
        success_url: Page's URL where the client will be redirected on success.
        template_name: Django template is used for rendering page.

    """
    
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'registration/register.html'


def profile(req: HttpRequest) -> HttpResponse:
    """Render the current user's personal page.
    
    Args:
        req (HttpRequest): HTTP request from client's browser.
        
    Returns:
        HttpResponse: HTTP response to the client with rendered HTML page.

    """
    context = {'title': 'homepage', 'render_user': req.user}

    if hasattr(req.user, 'profile') and req.user.profile:
        profile: Profile = req.user.profile

        context['can_edit'] = profile.can_be_edited(by=req.user)
        context['followers'] = profile.followers.all()
        context['following'] = profile.following.all()

    return render(req, 'registration/profile.html', context)


class ProfileUpdate(UpdateView):
    """Handles profile editing.

    Attributes:
        form_class: Django form is displayed on the page.
        template_name: Django template is used for rendering page.
        object: instanse of the updated Profile.
        
    """

    form_class = ProfileChangeForm
    template_name = 'users/profileUpdate.html'

    object: Profile | None

    def get_object(self, queryset=None):
        """Retrieve Profile instanse from the DB.

        Args:
            queryset (_type_, optional): _description_. Defaults to None.

        Raises:
            Http404: Profile couldn't be found or current user is unauthorized.

        Returns:
            Profile: Returns found profile instanse.

        """
        user_id: int = self.kwargs['user_id']

        User = get_user_model()

        user = get_object_or_404(User, pk=user_id)
        profile: Profile = user.profile

        if profile.can_be_edited(by=self.request.user):
            return profile
        else:
            raise Http404

    def form_valid(self: ProfileUpdate, form: ProfileChangeForm):
        """Schedule avatar processing task on form validation success.

        Args:
            self (ProfileUpdate): instanse of ProfileUpdate.
            form (ProfileChangeForm): form with validated data.

        Returns:
            HttpResponse: HTTP response redirects the client on success page.

        """
        response = super().form_valid(form)

        profile = self.object

        # result: AsyncResult[bool] = process_avatar.delay(profile.pk)
        process_avatar.delay(profile.pk)

        return response

    def get_success_url(self):
        """Get success url for client redirection.

        Returns:
            _type_: URL where the client will be redirected.

        """
        return reverse_lazy('users:profile')


def detail(req: HttpRequest, user_id: int) -> HttpResponse:
    """Render user's profile if the current one is unauthorized.

    Args:
        req (HttpRequest): HTTP request from client's browser.
        user_id (int): ID of the user will be shown.

    Raises:
        Http404: Profile couldn't be found or current user is unauthorized.

    Returns:
        HttpResponse: HTTP response to the client with rendered HTML page.

    """    
    user_model = get_user_model()
    other_user = get_object_or_404(user_model, pk=user_id)

    other_profile: Profile = other_user.profile
    profile: Profile = req.user.profile

    if not other_profile.can_be_seen(by=req.user):
        raise Http404

    context = {
        'title': 'homepage',
        'render_user': other_user,
        'can_edit': profile.can_be_edited(req.user),
        'can_follow': req.user != other_user,
        'is_followed': other_profile.is_followed(by=profile),
        'followers': other_profile.followers.all(),
        'following': other_profile.following.all(),
    }

    return render(req, 'registration/profile.html', context)


@login_required
def toggle_follow(req: HttpRequest, user_id: int):
    """Switch user following relation.

    Args:
        req (HttpRequest): HTTP request from client's browser.
        user_id (int): ID of the user will be followed/unfollowed.

    Raises:
        Http404: Profile couldn't be found or current user is unauthorized.

    Returns:
        HttpResponse: HTTP response redirects the client to the target profile.

    """
    user_model = get_user_model()
    user_target = get_object_or_404(user_model, pk=user_id)

    if not hasattr(user_target, 'profile') or not isinstance(
        user_target.profile, Profile
    ):
        raise Http404

    if not hasattr(req.user, 'profile') or not isinstance(
        req.user.profile, Profile
    ):
        raise Http404

    profile_target = user_target.profile
    profile = req.user.profile

    if not profile.can_be_seen(profile_target):
        raise Http404

    follow_rel = Follow.objects.filter(
        follower=profile, followee=profile_target
    )

    if follow_rel.exists():
        profile.unfollow(profile_target)
    else:
        profile.follow(profile_target)

    return redirect('users:detail', user_id=user_id)
