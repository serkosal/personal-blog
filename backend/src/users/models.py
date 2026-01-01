from django.contrib.auth.models import AbstractBaseUser

from django.conf import settings
from django.db import models



# Create your models here.
class Profile(models.Model):
    
    def user_directory_path(profile: Profile, filename: str) -> str:
        return f'users/{profile.user.pk}/{filename}'
    
    user: AbstractBaseUser = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False
    )
    
    avatar = models.ImageField(
        null=True,
        upload_to=user_directory_path,
    )