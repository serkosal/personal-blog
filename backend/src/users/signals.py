from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(
    sender: type[AbstractUser], 
    instance: AbstractUser, 
    created: bool,
    **kwargs
) -> None:
    '''
    This method is registered to automatically created profiles when new User's
    instances created
    
    :param sender: Signal sender
    :type sender: type[AbstractUser]
    :param instance: instance of the saved model. In our case it's User model
    :type instance: AbstractUser
    :param created: Is model successfully saved or not
    :type created: bool
    :param kwargs: Description
    '''
    if created:
        Profile.objects.create(user=instance)


def create_profiles_for_existing_users(sender, **kwargs) -> None:
    
    '''
    This method is registered to automatically created profiles for existing 
    users without profiles
    
    :param sender: Signal sender
    :param kwargs: Other key-value arguments
    '''
    
    User: AbstractUser = get_user_model()
    
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)