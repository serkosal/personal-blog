from django.db import models

# from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
class Post(models.Model):
    
    # author field
    # author = AbstractBaseUser
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    started_at = models.DateTimeField()
    last_edited = models.DateTimeField()
    published_at = models.DateTimeField()
    
    is_published = models.BooleanField() 