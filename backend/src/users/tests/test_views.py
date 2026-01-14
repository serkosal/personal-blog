from users.tests.base import BaseUsersViews
    

class MyProfileTest(BaseUsersViews):
    
    url = '/accounts/profile/'
    edit_link='<a href="/accounts/profile/{user.pk}/e/">edit</a>'

    def test_open_anon_user(self):
        resp = self.get_response()
        
        self.assertContains(
            resp,
            'You are not logged into your account!',
        )
    
        
    def test_open_pub_user(self):
        user = self.pub1.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response()
        
        self.assertContains(
            resp, 
            self.edit_link.format(user=user)
        )

        
    def test_open_priv_user(self):
        user = self.priv.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response()
        
        self.assertContains(resp, self.edit_link.format(user=user))
    
    
    def test_open_deact_user(self):
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
    
    url = '/accounts/profile/{user.pk}/'
    edit_link='<a href="/accounts/profile/{user.pk}/e/">edit</a>'
    
    # self
    def test_public_user(self):
        user = self.pub1.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response(user=user)
        
        self.assertContains(resp, self.edit_link.format(user=user)) # edit btn

        
    def test_private_user(self):
        user = self.priv.user
        
        self.assertTrue(self.login(user))
        resp = self.get_response(user=user)
        
        self.assertContains(resp, self.edit_link.format(user=user)) # edit btn
    
    
    def test_deact_user(self):
        user = self.deact.user
        
        self.assertFalse(self.login(user))
        resp = self.get_response(user=user)
        
        self.assertEqual(resp.status_code, 404)
    
    
    # users interactions
    def test_private_on_public(self):
        target = self.pub1.user
        actor = self.priv.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertNotContains(resp, self.edit_link.format(user=target)) # edit btn
    
    
    def test_public_on_private(self):
        target = self.priv.user
        actor = self.pub1.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
        
    
    def test_admin_on_private(self):
        target = self.priv.user
        actor = self.admin.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertContains(resp, self.edit_link.format(user=target)) # edit btn
    
    
    def test_deact_admin_on_private(self):
        target = self.priv.user
        actor = self.deact_admin.user
        
        self.assertFalse(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
        
        
    def test_public_on_deact(self):
        target = self.deact.user
        actor = self.pub1.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
    
    
    def test_admin_on_deact(self):
        target = self.deact.user
        actor = self.admin.user
        
        self.assertTrue(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertContains(resp, self.edit_link.format(user=target)) # edit btn
        
        
    def test_deact_admin_on_deact(self):
        target = self.deact.user
        actor = self.deact_admin.user
        
        self.assertFalse(self.login(actor))
        resp = self.get_response(user=target)
        
        self.assertEqual(resp.status_code, 404)
    
# class ProfileUpdate(BaseUsersForTests):
#     pass