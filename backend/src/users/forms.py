"""file with forms for 'users' Django's app."""

from django import forms

from .models import Profile


class ProfileChangeForm(forms.ModelForm):
    """Specifies the form for changing user profiles by themselves."""
    
    class Meta:
        """Specifies which fields of the Profile could be changed.
        
        Attributes:
            model: a model class for forms.ModelForm.
            fields: Profile fields which will be in the form.

        """
        
        model = Profile
        fields = ['avatar', 'bio', 'is_private']
