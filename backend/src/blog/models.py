from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


# custom model manager
class PostManager(models.Manager):
    def visible_to(self, user: AbstractUser):
        posts = self.get_queryset()

        if user.is_authenticated:
            if user.has_perm('blog.see_others_unpublished'):
                return posts
            else:
                return posts.filter(Q(author=user) | Q(is_published=True))

        return posts.filter(is_published=True)

    def editable_to(self, user: AbstractUser):
        posts = self.get_queryset()

        if user.is_anonymous:
            return posts.none()

        if user.has_perm('blog.edit_others'):
            return posts

        return posts.filter(Q(author=user) | Q(is_published=True))


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    title = models.CharField(
        max_length=100, null=False, blank=True, default='Title'
    )

    # rewrite to a custom json Field
    def content_default():
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
        permissions = (
            (
                'blog.see_others_unpublished',
                "Users could see other user's unpublished post",
            ),
            ('blog.edit_others', "Users could edit other user's post"),
        )

    def __str__(self) -> str:
        return f'Post author: {self.author} title: {self.title}'

    def can_edit(self, user: AbstractUser) -> bool:
        return (
            user.is_authenticated
            and user.is_active
            and (user == self.author or user.has_perm('blog.edit_others'))
        )
