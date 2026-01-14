"""file with forms for 'blog' Django app."""

from django import forms

from blog.models import Post

from .widgets import PostContentWidget


class PostCreateForm(forms.ModelForm):
    """Form for post creation."""
    
    class Meta:
        """Metadata for ModelForm."""
        
        model = Post
        fields = ['title', 'is_published']


class PostEditForm(forms.ModelForm):
    """Form for post editing."""
    
    class Meta:
        """Metadata for ModelForm."""
        
        model = Post
        fields = ['title', 'content', 'tags', 'is_published']
        widgets = {'content': PostContentWidget()}
