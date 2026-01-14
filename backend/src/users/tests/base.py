"""file with base classes for users tests."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.test import TestCase

from users.models import Profile


class BaseUsersForTests(TestCase):
    """Base class with users for tests."""
    # this method is faster than SetUp, because it's created just once for class
    # init the users for testing
    @classmethod
    def setUpTestData(cls):
        """Init test data once per for class test."""
        cls.user_model = get_user_model()
        cls.usernames = (
            "pub1", "pub2", "priv", "admin",
            "deact", "anon", "deact_admin"
        )
        
        cls.users = {
            username: cls.user_model(username=username) 
            for username in cls.usernames
            if username != "anon"
        }

        cls.users["admin"].is_superuser = True
        cls.users["deact"].is_active = False
        cls.users["deact_admin"].is_superuser = True
        cls.users["deact_admin"].is_active = False
        
        for value in cls.users.values():
            value.set_password(raw_password="test")
            value.save()
        
        cls.users["anon"] = AnonymousUser()

        cls.pub1: Profile  = cls.users["pub1"].profile
        cls.pub2: Profile  = cls.users["pub2"].profile
        cls.priv: Profile  = cls.users["priv"].profile
        cls.admin: Profile = cls.users["admin"].profile
        cls.deact: Profile = cls.users["deact"].profile
        cls.deact_admin: Profile = cls.users["deact_admin"].profile
        
        cls.priv.is_private = True
        cls.priv.save()


class BaseUsersViews(BaseUsersForTests):
    """Base class for testing users.views."""
    
    url: str
    
    def login(self, user: AbstractUser | None = None):
        """Log in specified user."""
        return self.client.login(username=user.username, password="test")
                
    def get_response(self, *args, **kwargs):
        """Get response for class's URL."""
        return self.client.get(self.url.format(*args, **kwargs))