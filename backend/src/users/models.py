from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db import models



# Create your models here.
class Profile(models.Model):
    
    def user_directory_path(profile: Profile, filename: str) -> str:
        return f'users/{profile.user.pk}/avatars/{filename}'
    
    user: AbstractUser = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False
    )
    
    avatar = models.ImageField(
        null=True,
        default='users/default_avatar.png',
        upload_to=user_directory_path,
    )
    
    bio = models.TextField(max_length=200, null=False, blank=True, default="")
    
    is_private = models.BooleanField(
        default=False
    )
    
    class Meta:
        permissions = (
            ("users.see_private", "Users can see other user's profiles"),
            ("users.edit_others", "Users can edit other user's profiles")
        )

    def __str__(self) -> str:
        return f'Profile (username: {self.user}, user id: {self.user.pk})'

    def can_see(self, user: AbstractUser):
        
        return not self.is_private or user.is_authenticated and (
            user == self.user or
            user.is_active and user.has_perm("users.see_private")
        )
    
    def can_edit(self, user: AbstractUser) -> bool:
        return user.is_authenticated and user.is_active and (
            user == self.user or
            user.has_perm("users.edit_others")
        )