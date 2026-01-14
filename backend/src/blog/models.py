"""file with URL patterns for 'blog' Django app."""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from taggit.managers import TaggableManager


class PostManager(models.Manager):
    """Custom Profile's model manager."""
    
    def visible_to(self, user: AbstractUser):
        """Check if user can see the post.

        Args:
            self (PostManager): instance of PostManager.
            user (AbstractUser): user is checked for post visibility.

        Returns:
            bool: True if user can see the post.

        """
        posts = self.get_queryset()

        if user.is_authenticated:
            if user.has_perm('blog.see_others_unpublished'):
                return posts
            else:
                return posts.filter(Q(author=user) | Q(is_published=True))

        return posts.filter(is_published=True)

    def editable_to(self, user: AbstractUser):
        """Check if user can edit the post.
        
        Args:
            self (PostManager): instance of PostManager.
            user (AbstractUser): user is checked for post visibility.

        Returns:
            bool: True if user can edit the post.

        """
        posts = self.get_queryset()

        if user.is_anonymous:
            return posts.none()

        if user.has_perm('blog.edit_others'):
            return posts

        return posts.filter(Q(author=user) | Q(is_published=True))


class Post(models.Model):
    """Django model for posts.
    
    Attributes:
        author: user who wrote the post.
        title: title of the post.
        content: JSON formated post content returned by EditorJs library.
        started_at: datetime when post was created. 
        last_edited: datetime when post was edited last time.
        published_at: datetime when post was first published.
        is_published: Has post been published?
        posts: PostManager acts like objects, but also has additional methods.

    """
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    title = models.CharField(
        max_length=100, null=False, blank=True, default='Title'
    )
    
    tags = TaggableManager()

    # rewrite to a custom json Field
    def content_default():
        """Get post's default content data."""
        return {'content': {}}

    content = models.JSONField(null=False, blank=False, default=content_default)

    started_at = models.DateTimeField(
        null=False, blank=False, auto_now_add=True
    )
    last_edited = models.DateTimeField(null=True, blank=False, auto_now=True)
    published_at = models.DateTimeField(null=True, blank=False)

    is_published = models.BooleanField(default=False)

    posts = PostManager()

    class Meta:
        """Permissions for Post model."""
        
        permissions = (
            (
                'blog.see_others_unpublished',
                "Users could see other user's unpublished post",
            ),
            ('blog.edit_others', "Users could edit other user's post"),
        )

    def __str__(self) -> str:
        """Return string representation of the post.
        
        Args:
            self (Post): Post instance.

        """
        return f'Post author: {self.author} title: {self.title}'

    def can_edit(self, user: AbstractUser) -> bool:
        """Check if user can edit the post.
        
        Args:
            self (Post): Post instance.
            user (AbstractUser): user is checked for ability to edit a post.
        
        """
        return (
            user.is_authenticated
            and user.is_active
            and (user == self.author or user.has_perm('blog.edit_others'))
        )
