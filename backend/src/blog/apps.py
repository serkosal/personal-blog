"""file with config for the 'blog' Django app."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Encapsulates configuration for the 'blog' app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
