from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self) -> None:
        from .signals import (
            create_user_profile, 
            create_profiles_for_existing_users
        )
        
        post_migrate.connect(create_profiles_for_existing_users, sender=self)
        