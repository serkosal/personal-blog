from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Post(models.Model):
    
    # author field
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True
    )
    
    title = models.CharField(max_length=100, null=False, blank=True, default="Title")
    
    # change to JSON field
    content = models.TextField(null=False, blank=False, default="Blog content")
    
    started_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    last_edited = models.DateTimeField(null=True, blank=False, auto_now=True)
    published_at = models.DateTimeField(null=True, blank=False)
    
    is_published = models.BooleanField(default=False) 
    
    
    class Meta:
        permissions = (
            ("blog.see_others_unpublished", "Users could see other user's unpublished post"),
            ("blog.edit_others", "Users could edit other user's post")
        )
    
    def __str__(self) -> str:
        return f'Post author: {self.author} title: {self.title}'
    
    
    def can_see(self, user: AbstractUser) -> bool:
        
        return self.is_published or (
            user.is_authenticated and (
                user == self.author or
                user.has_perm("blog.see_others_unpublished")
            )
        )


    def can_edit(self, user: AbstractUser) -> bool:
        
        return user.is_authenticated and (
            user == self.author or
            user.has_perm("blog.edit_others")
        )