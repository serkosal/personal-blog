"""file with configuration for 'users' Django app."""

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    """Incapsulates configuration for Django 'users' application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self) -> None:
        """Import and register signals when the Django core is ready."""
        from .signals import (  # noqa: PLC0415
            create_profiles_for_existing_users,
            create_user_profile,  # noqa: F401
        )

        post_migrate.connect(create_profiles_for_existing_users, sender=self)
