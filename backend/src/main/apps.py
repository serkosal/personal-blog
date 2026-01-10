"""file with configation of the main Django app."""

from django.apps import AppConfig


class MainConfig(AppConfig):
    """Encapsulates Django application configuration."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
