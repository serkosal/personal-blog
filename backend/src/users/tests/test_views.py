"""file with tests for users.views."""

from users.tests.base import BaseUsersViews
    

class MyProfileTest(BaseUsersViews):
    """Tests my profile view."""
    
    url = '/accounts/profile/'
    edit_link='<a href="/accounts/profile/{user.pk}/e/">edit</a>'

    def test_open_anon_user(self):
        """Test anonymous user goes to the 'view my profile' url."""
        resp = self.get_response()
        
        self.assertContains(
            resp,
            'You are not logged into your account!',
        )
    
        
    def test_open_pub_user(self):
        """Test public profile goes to the 'view my profile' url."""
        user = self.pub1.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response()
        
        self.assertContains(
            resp, 
            self.edit_link.format(user=user)
        )

        
    def test_open_priv_user(self):
        """Test private profile goes to the 'view my profile' url."""
        user = self.priv.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response()
        
        self.assertContains(resp, self.edit_link.format(user=user))
    
    
    def test_open_deact_user(self):
        """Test deactivated profile goes to the 'view my profile' url."""
        user = self.deact.user
        
        self.assertFalse(self.login(user))
        resp = self.get_response()
        
        self.assertContains(
            resp, 
            'You are not logged into your account!'
        )
        self.assertNotContains(resp, self.edit_link.format(user=user))
    
    # test followers
        

class ProfileDetail(BaseUsersViews):
    """Tests profile detail view."""
    
    # TODO:
    # test anon users
    
    url = '/accounts/profile/{user.pk}/'
    edit_link='<a href="/accounts/profile/{user.pk}/e/">edit</a>'
    
    # self
    def test_public_user(self):
        """Test can public profile get his own profile."""
        user = self.pub1.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response(user=user)
        
        self.assertContains(resp, self.edit_link.format(user=user)) # edit btn

        
    def test_private_user(self):
        """Test can private profile get his own profile."""
        user = self.priv.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response(user=user)
        
        self.assertContains(resp, self.edit_link.format(user=user)) # edit btn
    
    
    def test_deact_user(self):
        """Test can deactivated profile get his own profile."""
        user = self.deact.user
        
        self.assertFalse(self.login(user))
        resp = self.get_response(user=user)
        
        self.assertEqual(resp.status_code, 404)
    
    
    # users interactions
    def test_private_on_public(self):
        """Test can private profile get public's one."""
        target = self.pub1.user
        actor = self.priv.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        # edit btn
        self.assertNotContains(resp, self.edit_link.format(user=target)) 
    
    
    def test_public_on_private(self):
        """Test can public profile get private's one."""
        target = self.priv.user
        actor = self.pub1.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
        
    
    def test_admin_on_private(self):
        """Test can admin get private profile."""
        target = self.priv.user
        actor = self.admin.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertContains(resp, self.edit_link.format(user=target)) # edit btn
    
    
    def test_deact_admin_on_private(self):
        """Test can deactivated admin get private profile."""
        target = self.priv.user
        actor = self.deact_admin.user
        
        self.assertFalse(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
        
        
    def test_public_on_deact(self):
        """Test can public profile get deactivated profile."""
        target = self.deact.user
        actor = self.pub1.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
    
    
    def test_admin_on_deact(self):
        """Test can admin get deactivated profile."""
        target = self.deact.user
        actor = self.admin.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertContains(resp, self.edit_link.format(user=target)) # edit btn
        
        
    def test_deact_admin_on_deact(self):
        """Test can deactivated admin get deactivated profile."""
        target = self.deact.user
        actor = self.deact_admin.user
        
        self.assertFalse(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
    
# class ProfileUpdate(BaseUsersForTests):
#     pass