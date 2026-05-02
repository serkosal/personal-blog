"""file with forms for 'blog' Django app."""

from django import forms
from django.forms.fields import BooleanField
from django.utils import timezone
from taggit.forms import TagField

from blog.models import Post
from .widgets import PostContentWidget


class PostCreateForm(forms.ModelForm):
    """Form for post creation."""
    
    is_published = BooleanField(initial=False, required=False)
    
    class Meta:
        """Metadata for ModelForm."""
        
        model = Post
        fields = ['title', 'slug']


class PostEditForm(forms.ModelForm):
    """Form for post editing."""
    
    is_published = BooleanField(required=False)
    tags = TagField(required=True)
    
    class Meta:
        """Metadata for ModelForm."""
        
        model = Post
        fields = ['title', 'slug', 'content', 'tags']
        widgets = {'content': PostContentWidget()}

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.instance: Post
            self.fields['is_published'].initial = bool(self.instance.published_at)
            
            
    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('is_published'):
            if not instance.published_at:
                instance.published_at = timezone.now()
        else:
            instance.published_at = None

        if commit:
            instance.save()

        return instance