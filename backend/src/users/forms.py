from django import forms

from .models import Profile


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'is_private']
