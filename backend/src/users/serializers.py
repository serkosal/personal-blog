"""file with serializers for user related Django's models."""

from django.conf import settings
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Specifies a DRF's model serializer for User model."""
    
    class Meta:
        """Specifies a metadata for DRF's ModelSerializer."""
        
        model = settings.AUTH_USER_MODEL
        fields = '__all__'
