"""file with tests for 'users' Django's app."""

from django.test import TestCase
from users.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

# Create your tests here.

# registration test
# login test 
# password change test
# check authentification rights

# region Base test classes

class BaseProfilePermissionsTests(TestCase):
    
    def setUp(self):
        self.user_model = get_user_model()
        self.usernames = (
            "pub1", "pub2", "priv", "admin",
            "deact", "anon", "deact_admin"
        )
        
        self.users = {
            username: self.user_model(username=username, password="test") 
            for username in self.usernames
            if username != "anon"
        }

        self.users["admin"].is_superuser = True
        self.users["deact"].is_active = False
        self.users["deact_admin"].is_superuser = True
        self.users["deact_admin"].is_active = False
        
        for value in self.users.values(): 
            value.save()
        
        self.users["anon"] = AnonymousUser()
        

        self.pub1: Profile  = self.users["pub1"].profile
        self.pub2: Profile  = self.users["pub2"].profile
        self.priv: Profile  = self.users["priv"].profile
        self.admin: Profile = self.users["admin"].profile
        self.deact: Profile = self.users["deact"].profile
        self.deact_admin: Profile = self.users["deact_admin"].profile
        
        self.priv.is_private = True
        self.priv.save()

# endregion

class ProfileTests(TestCase):
    
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

class ProfileCanSeeTests(BaseProfilePermissionsTests):
    
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

class ProfileCanEditTests(BaseProfilePermissionsTests):
    
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
