"""file with signals for 'users' Django's app."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(
    sender: type[AbstractUser], instance: AbstractUser, created: bool, **kwargs
) -> None:
    """Create profiles for newly created User's instances.
    
    This method is registered to be called when new user's instances are saved 
    in the database.
    
    Args:
        sender: Signal sender.
        instance (AbstractUser): instance of the saved User's model.
        created (bool): Was the model saved successfully?
        **kwargs: keyword arguments.

    """
    if created:
        Profile.objects.create(user=instance)


def create_profiles_for_existing_users(sender, **kwargs) -> None:
    """Create profiles for users without profiles.
    
    This method is registered to be called when manage.py migrate is executed.

    Args:
        sender: Signal sender.
        kwargs: Arbitrary keyword arguments.

    """
    User: AbstractUser = get_user_model()

    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
