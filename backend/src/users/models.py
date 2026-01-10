"""file with database models for 'users' Django's app."""

from pathlib import Path

from django.conf import settings

# from django.core.files.storage import default_storage
# from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Profile(models.Model):
    """Extends django's default User class.
    
    Attributes:
        user: primary key to User's model with OneToOne relationship.
        avatar: stores path to the the original unprocessed avatar.
        AVATAR_SIZES: specifies avatar's sizes.
        avatar_is_set: specifies if avatar was already processed.
        bio: user's description of themself.
        is_private:
            specifies if profile could be seen by other unauthorized users.
        followers: users that following this one.

    """
    
    user: AbstractUser = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )

    AVATAR_SIZES = (1024, 512, 256, 128, 64)

    def user_avatar_path(self: Profile, filename: str) -> str:
        """Return path where avatar will be stored.

        Args:
            self (Profile): instanse of Profile
            filename (str): avatar's filename

        Returns:
            str: path to the specified filename

        """
        return f'users/{self.user.pk}/avatars/{filename}'

    @property
    def processed_avatar_pathes(self) -> list[Path]:
        """Return list of pathes with processed avatar's images.

        Returns:
            list[Path]: list of pathes with processed avatar's images

        """
        return [
            self.user_avatar_path(f'{size}.webp')
            for size in Profile.AVATAR_SIZES
        ]

    @property
    def avatar_img_attrs(self) -> str:
        """Return html img tag attributes.

        Returns:
            str: with following attributes: src, srcset, alt, style

        """
        src: str
        base_path: str
        alt = f"{self.user.username}'s avatar"
        if self.avatar_is_set:
            base_path = f'/media/users/{self.user.pk}/avatars/'
            src = base_path + '64.webp'
        else:
            base_path = '/static/users/avatars/'
            src = base_path + 'default_avatar_64.webp'

        srcset_list = [
            base_path + f'{sz}.webp'
            if self.avatar_is_set
            else base_path + f'default_avatar_{sz}.webp'
            for sz in Profile.AVATAR_SIZES
        ]

        srcset = ', '.join(srcset_list)

        return f'''
            src="{src}" 
            srcset="{srcset}"
            alt="{alt}" 
            style="border-radius: 100%;"
        '''

    avatar = models.ImageField(null=True, upload_to=user_avatar_path)
    # if avatar is set, then avatar should be null (file deleted),
    # and different sized avatar's files are already created and is ok
    avatar_is_set = models.BooleanField(null=False, default=False)

    bio = models.TextField(max_length=200, null=False, blank=True, default='')

    is_private = models.BooleanField(default=False)

    followers = models.ManyToManyField(
        'self',
        through='Follow',
        through_fields=('followee', 'follower'),
        related_name='following',
        symmetrical=False,
        blank=True,
    )

    class Meta:
        """Stores permissions for the Profile model."""
        
        permissions = (
            ('users.see_private', "Users can see other user's profiles"),
            ('users.edit_others', "Users can edit other user's profiles"),
        )

    def __str__(self) -> str:
        """Represent the Profile class as a string.

        Returns:
            str: Profile representation with user's nickname and id. 

        """
        return f'Profile (username: {self.user}, user id: {self.user.pk})'

    def can_be_seen(self, by: AbstractUser | Profile) -> bool:
        """Return True if the given profile can see this one.
        
        Args:
            by (AbstractUser | Profile): the user whose ability to see 
            this profile is checked.

        Raises:
            ValueError: raised when 'by' is not an instanse of AbstractUser 
            or Profile.

        Returns:
            bool: True if this profile can be seen.

        """
        if isinstance(by, AbstractUser):
            by_user = by
        elif isinstance(by, Profile):
            by_user = by.user
        else:
            raise ValueError(
                "'by' must be instance of 'AbstractUser' or 'Profile'!"
            )

        return (
            not self.is_private
            or by_user.is_authenticated
            and (
                by_user == self.user
                or by_user.is_active
                and by_user.has_perm('users.see_private')
            )
        )

    def can_be_edited(self, by: AbstractUser | Profile) -> bool:
        """Return True if the given user can edit this one.
        
        Args:
            by: the user whose ability to edit this profile is being checked.

        Raises:
            ValueError: raised when 'by' is not an instanse of AbstractUser 
            or Profile

        Returns:
            bool: True if this profile can be edited

        """
        if isinstance(by, AbstractUser):
            by_user = by
        elif isinstance(by, Profile):
            by_user = by.user
        else:
            raise ValueError(
                "'by' must be instance of 'AbstractUser' or 'Profile'!"
            )

        return (
            by_user.is_authenticated
            and by_user.is_active
            and (by_user == self.user or by_user.has_perm('users.edit_others'))
        )

    def is_following(self, target: Profile) -> bool:
        """Check whether this user follows the target.
        
        Args:
            target (Profile): the user who's checked for following this profile.

        Returns:
            bool: True if target is following

        """
        return Follow.objects.filter(follower=self, followee=target).exists()

    def is_followed(self, by: Profile) -> bool:
        """Check whether the given profile follows this one.
        
        Args:
            self (Profile): this user. 
            by (Profile): the user whose following to this profile is checked.

        Returns:
            bool: True if 'by' follows this one.

        """
        return Follow.objects.filter(follower=by, followee=self).exists()

    def follow(self, target: Profile):
        """Follow the given user.
        
        Args:
            target (Profile): the user who will be followed by this profile.
        
        """
        if self != target:
            Follow.objects.create(followee=target, follower=self)

    def unfollow(self, target: Profile):
        """Unfollow the given user.
        
        Args:
            target (Profile): the user who will be unfollowed by this profile.
        
        """
        Follow.objects.filter(followee=target, follower=self).delete()


class Follow(models.Model):
    """Represents follow relationship.
    
    Attributes:
        followee: the user that's FOLLOWED BY OTHER user(s).
        follower: the user that is FOLLOWING other user.
    
        created_at: datetime when the relation was created.

    """

    followee = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='follower_relations'
    )
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='following_relations'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Specifies unique constraints for the 'Follow' relationships."""
        
        unique_together = ('followee', 'follower')
