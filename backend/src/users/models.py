from pathlib import Path

# from django.core.files.storage import default_storage
# from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models



# Create your models here.
class Profile(models.Model):
    
    user: AbstractUser = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False
    )
    
    AVATAR_SIZES = (1024, 512, 256, 128, 64)
    
    def user_directory_path(profile: Profile, filename: str) -> str:
        return f'users/{profile.user.pk}/avatars/{filename}'
    
    @property
    def processed_avatar_pathes(self) -> list[Path]:
        return [
            Profile.user_directory_path(self, f'{size}.webp') 
            for size in Profile.AVATAR_SIZES
        ]
        
    @property 
    def avatar_img_attrs(self) -> str:
        
        src:str
        base_path: str
        alt = f"{self.user.username}'s avatar"
        if self.avatar_is_set:
            base_path = f'/media/users/{self.user.pk}/avatars/'
            src = base_path + '64.webp'
        else:
            base_path = '/static/users/avatars/'
            src = base_path + 'default_avatar_64.webp'
        
        srcset_list = [
            base_path + f'{sz}.webp' if self.avatar_is_set 
            else base_path + f'default_avatar_{sz}.webp' 
            for sz in Profile.AVATAR_SIZES
        ]
        
        srcset = ", ".join(srcset_list)
            
        return f'''
            src="{src}" 
            srcset="{srcset}"
            alt="{alt}" 
            style="border-radius: 100%;"
        '''
    
    avatar = models.ImageField(
        null=True,
        upload_to=user_directory_path
    )
    # if avatar is set, then avatar should be null (file deleted),
    # and different sized avatar's files are already created and is ok
    avatar_is_set = models.BooleanField(null=False, default=False)
    
    bio = models.TextField(max_length=200, null=False, blank=True, default="")
    
    is_private = models.BooleanField(
        default=False
    )
    
    followers = models.ManyToManyField(
        "self",
        through="Follow",
        through_fields=("followee", "follower"),
        related_name="following",
        symmetrical=False,
        blank=True
    )
    
    
    class Meta:
        permissions = (
            ("users.see_private", "Users can see other user's profiles"),
            ("users.edit_others", "Users can edit other user's profiles")
        )

    def __str__(self) -> str:
        return f'Profile (username: {self.user}, user id: {self.user.pk})'


    def can_be_seen(self, by: AbstractUser | Profile):
        
        if isinstance(by, AbstractUser):
            by_user = by
        elif isinstance(by, Profile):
            by_user = by.user
        else:
            raise ValueError(
                "'by' must be instance of 'AbstractUser' or 'Profile'!"
            )
        
        return not self.is_private or by_user.is_authenticated and (
            by_user == self.user or
            by_user.is_active and by_user.has_perm("users.see_private")
        )
    
    
    def can_be_edited(self, by: AbstractUser | Profile) -> bool:
        
        if isinstance(by, AbstractUser):
            by_user = by
        elif isinstance(by, Profile):
            by_user = by.user
        else:
            raise ValueError(
                "'by' must be instance of 'AbstractUser' or 'Profile'!"
            )
        
        return by_user.is_authenticated and by_user.is_active and (
            by_user == self.user or
            by_user.has_perm("users.edit_others")
        )
    
    
    def is_following(self, target: Profile):
        return Follow.objects.filter(follower=self, followee=target).exists()
    
    
    def is_followed(self, by: Profile):
        return Follow.objects.filter(follower=by, followee=self).exists()
    
    
    def follow(self, target: Profile):
        if self != target:
            Follow.objects.create(followee=target, follower=self)
    
    
    def unfollow(self, target: Profile):
        Follow.objects.filter(followee=target, follower=self).delete()


class Follow(models.Model):
    followee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_relations")
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following_relations")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("followee", "follower")