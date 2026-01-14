"""file with tests for 'users' Django's app."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from users.models import Profile
from users.tests.base import BaseUsersForTests


class Creation(TestCase):
    """Test profiles creation."""
    @classmethod
    def setUpTestData(self):
        """Init tests once for class creation."""
        self.user_model = get_user_model()
    
    def test_user_creation(self):
        """Test user creation."""
        self.assertEqual(self.user_model.objects.all().count(), 0)
        user = self.user_model(username="test", password="test")
        user.save()
        self.assertEqual(self.user_model.objects.all().count(), 1)
    
    
    def test_profile_creation_on_user_creation(self):
        """Test creation of profiles on users creation."""
        self.assertEqual(Profile.objects.all().count(), 0)
        
        user = self.user_model(username="test", password="test")
        user.save()
        
        self.assertEqual(Profile.objects.all().count(), 1)

# region permissions tests

class CanSee(BaseUsersForTests):
    """Test visibility of profiles."""
    
    # users' ability to see themselves
    def test_public_can_see_itself(self):
        """Test public profiles can see themselves."""
        self.assertTrue(self.pub1.can_be_seen(by=self.pub1))
    
    def test_private_can_see_itself(self):
        """Test private profiles can see themselves."""
        self.assertTrue(self.priv.can_be_seen(by=self.priv))
        
    def test_deact_cant_see_itself(self):
        """Test deact profiles cant see themselves."""
        self.assertFalse(self.deact.can_be_seen(by=self.deact))
        
    def test_deact_admin_cant_see_itself(self):
        """Test deact admins cant see themselves."""
        self.assertFalse(self.deact_admin.can_be_seen(by=self.deact_admin))
    
    
    # check ability to see public profiles
    def test_public_can_see_public(self):
        """Test public profiles can see other public profiles."""
        self.assertTrue(self.pub1.can_be_seen(by=self.pub2))
        self.assertTrue(self.pub2.can_be_seen(by=self.pub1))
    
    def test_private_can_see_public(self):
        """Test profile's privacy doesn't affect visibility of public users."""
        self.assertTrue(self.pub1.can_be_seen(by=self.priv))
        self.assertTrue(self.pub2.can_be_seen(by=self.priv))
     
    def test_deact_can_see_public(self):
        """Test deactivated users can see public profiles."""
        self.assertTrue(self.pub1.can_be_seen(by=self.deact))
        
    def test_anon_can_see_public(self):
        """Test anonymous users can see public profiles."""
        self.assertTrue(self.pub1.can_be_seen(by=self.users["anon"]))
        self.assertTrue(self.pub2.can_be_seen(by=self.users["anon"]))
    
    
    # check permissions to see private profiles
    def test_users_without_perms_cant_see_private(self):
        """Test users without permissions cant see private profiles."""
        self.assertFalse(self.priv.can_be_seen(by=self.pub1))
        self.assertFalse(self.priv.can_be_seen(by=self.pub2))
        self.assertFalse(self.priv.can_be_seen(by=self.users["anon"]))
        
    def test_users_with_perms_can_see_private(self):
        """Test users with permissions can see private profiles."""
        self.assertTrue(self.priv.can_be_seen(by=self.admin))
        self.assertTrue(self.priv.can_be_seen(by=self.priv))
        
    def test_deact_admin_cant_see_private(self):
        """Test deactivated admin cant see private profiles."""
        self.assertFalse(self.priv.can_be_seen(by=self.deact_admin))
    
    # permissions to see deactivated
    def test_users_without_perms_cant_see_deact(self):
        """Test that users without permissions cant see deactivated profiles."""
        self.assertFalse(self.deact.can_be_seen(by=self.pub1))
        self.assertFalse(self.deact.can_be_seen(by=self.pub2))
        self.assertFalse(self.deact.can_be_seen(by=self.priv))
        self.assertFalse(self.deact.can_be_seen(by=self.users["anon"]))
        
    def test_users_with_perms_can_see_deact(self):
        """Test that users with permissions can see deactivated profiles."""
        self.assertTrue(self.deact.can_be_seen(by=self.admin))    

class CanEdit(BaseUsersForTests):
    """Test ability to edit profiles."""
    
    # users' ability to edit themselves
    def test_public_can_edit_itself(self):
        """Test that public user can edit himself."""
        self.assertTrue(self.pub1.can_be_edited(by=self.pub1))
        
    def test_private_can_edit_itself(self):
        """Test that private user can edit himself."""
        self.assertTrue(self.priv.can_be_edited(by=self.priv))
        
    def test_deact_cant_edit_itself(self):
        """Test that deactivated admin cant edit himself."""
        self.assertFalse(self.deact.can_be_edited(by=self.deact))
        
    def test_deact_admin_cant_edit_itself(self):
        """Test that deactivated admin cant edit himself."""
        self.assertFalse(self.deact_admin.can_be_edited(by=self.deact_admin))
        
    # check permissions to edit other public profiles
    def test_without_perms_cant_edit_others(self):
        """Test that users without permissions cant edit others."""
        for editor in self.users.values():
            if editor.has_perm('users.edit_others'): 
                continue
            
            for edited in self.users.values():
                if edited.pk == editor.pk or isinstance(edited, AnonymousUser):
                    continue
                
                edited_profile: Profile = edited.profile
                self.assertFalse(edited_profile.can_be_edited(by=editor))
    
    def test_with_perms_can_edit_others(self):
        """Test that users with permissions can edit others."""
        for edited in self.users.values():
            if edited.pk == self.admin.pk or isinstance(edited, AnonymousUser):
                    continue
            
            edited_profile: Profile = edited.profile
            self.assertTrue(edited_profile.can_be_edited(by=self.admin))
    
    def test_deact_with_perms_cant_edit_other(self):
        """Test that deactivated admin cant edit others."""
        for edited in self.users.values():
            if (
                edited.pk == self.deact_admin.pk 
                or isinstance(edited, AnonymousUser
            )): 
                continue
            
            edited_profile: Profile = edited.profile
            self.assertFalse(edited_profile.can_be_edited(by=self.deact_admin))

# endregion
