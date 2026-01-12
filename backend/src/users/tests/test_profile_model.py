"""file with tests for 'users' Django's app."""

from django.test import TestCase
from users.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

# region Base test classes

class BaseTests(TestCase):
    
    # this method is faster than SetUp, because it's created just once for class
    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.usernames = (
            "pub1", "pub2", "priv", "admin",
            "deact", "anon", "deact_admin"
        )
        
        cls.users = {
            username: cls.user_model(username=username, password="test") 
            for username in cls.usernames
            if username != "anon"
        }

        cls.users["admin"].is_superuser = True
        cls.users["deact"].is_active = False
        cls.users["deact_admin"].is_superuser = True
        cls.users["deact_admin"].is_active = False
        
        for value in cls.users.values(): 
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

# endregion

class Creation(TestCase):
    
    def setUp(self):
        self.user_model = get_user_model()
    
    def test_user_creation(self):
        
        self.assertEqual(self.user_model.objects.all().count(), 0)
        user = self.user_model(username="test", password="test")
        user.save()
        self.assertEqual(self.user_model.objects.all().count(), 1)
    
    
    def test_profile_creation_on_user_creation(self):
        
        self.assertEqual(Profile.objects.all().count(), 0)
        
        user = self.user_model(username="test", password="test")
        user.save()
        
        self.assertEqual(Profile.objects.all().count(), 1)

# region permissions tests

class CanSee(BaseTests):
    
    # users' ability to see themselves
    def test_public_can_see_itself(self):
        self.assertTrue(self.pub1.can_be_seen(by=self.pub1))
    
    def test_private_can_see_itself(self):
        self.assertTrue(self.priv.can_be_seen(by=self.priv))
        
    def test_deact_cant_see_itself(self):
        self.assertFalse(self.deact.can_be_seen(by=self.deact))
        
    def test_deact_admin_cant_see_itself(self):
        self.assertFalse(self.deact_admin.can_be_seen(by=self.deact_admin))
    
    
    # check ability to see public profiles
    def test_public_can_see_public(self):
        self.assertTrue(self.pub1.can_be_seen(by=self.pub2))
        self.assertTrue(self.pub2.can_be_seen(by=self.pub1))
    
    def test_private_can_see_public(self):
        self.assertTrue(self.pub1.can_be_seen(by=self.priv))
        self.assertTrue(self.pub2.can_be_seen(by=self.priv))
     
    def test_deact_can_see_public(self):
        self.assertTrue(self.pub1.can_be_seen(by=self.deact))
        
    def test_anon_can_see_public(self):
        self.assertTrue(self.pub1.can_be_seen(by=self.users["anon"]))
        self.assertTrue(self.pub2.can_be_seen(by=self.users["anon"]))
    
    
    # check permissions to see private profiles
    def test_users_without_perms_cant_see_private(self):
        self.assertFalse(self.priv.can_be_seen(by=self.pub1))
        self.assertFalse(self.priv.can_be_seen(by=self.pub2))
        self.assertFalse(self.priv.can_be_seen(by=self.users["anon"]))
        
    def test_users_with_perms_can_see_private(self):
        self.assertTrue(self.priv.can_be_seen(by=self.admin))
        self.assertTrue(self.priv.can_be_seen(by=self.priv))
        
    def test_deact_users_perms_cant_see_private(self):
        self.assertFalse(self.priv.can_be_seen(by=self.deact_admin))
    
    # permissions to see deactivated
    def test_users_without_perms_cant_see_deact(self):
        self.assertFalse(self.deact.can_be_seen(by=self.pub1))
        self.assertFalse(self.deact.can_be_seen(by=self.pub2))
        self.assertFalse(self.deact.can_be_seen(by=self.priv))
        self.assertFalse(self.deact.can_be_seen(by=self.users["anon"]))
        
    def test_users_with_perms_can_see_deact(self):
        self.assertTrue(self.deact.can_be_seen(by=self.admin))    

class CanEdit(BaseTests):
    
    # users' ability to edit themselves
    def test_public_can_edit_itself(self):
        self.assertTrue(self.pub1.can_be_edited(by=self.pub1))
        
    def test_private_can_edit_itself(self):
        self.assertTrue(self.priv.can_be_edited(by=self.priv))
        
    def test_deact_cant_edit_itself(self):
        self.assertFalse(self.deact.can_be_edited(by=self.deact))
        
    def test_deact_admin_cant_edit_itself(self):
        self.assertFalse(self.deact_admin.can_be_edited(by=self.deact_admin))
        
    # check permissions to edit other public profiles
    def test_without_perms_cant_edit_others(self):
        
        for editor in self.users.values():
            if editor.has_perm('users.edit_others'): 
                continue
            
            for edited in self.users.values():
                if edited.pk == editor.pk or isinstance(edited, AnonymousUser):
                    continue
                
                edited_profile: Profile = edited.profile
                self.assertFalse(edited_profile.can_be_edited(by=editor))
    
    def test_with_perms_can_edit_others(self):
        for edited in self.users.values():
            if edited.pk == self.admin.pk or isinstance(edited, AnonymousUser):
                    continue
            
            edited_profile: Profile = edited.profile
            self.assertTrue(edited_profile.can_be_edited(by=self.admin))
    
    def test_deact_with_perms_cant_edit_other(self):
        for edited in self.users.values():
            if edited.pk == self.deact_admin.pk or isinstance(edited, AnonymousUser):
                    continue
            
            edited_profile: Profile = edited.profile
            self.assertFalse(edited_profile.can_be_edited(by=self.deact_admin))
        
        
# endregion
