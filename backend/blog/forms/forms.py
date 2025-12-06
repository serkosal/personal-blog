from django import forms


from blog.models import Post
from .widgets import PostContentWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "is_published"] 
        widgets = {
            "content": PostContentWidget()
        }