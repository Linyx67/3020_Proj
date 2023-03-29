
from django.test import TestCase
from django.urls import reverse, resolve
from hris_app import views


class TestUrls(TestCase):

    def test_home_url_resolves(self):
        url = reverse('hris:home')
        self.assertEqual(resolve(url).func, views.home)

    def test_login_url_resolves(self):
        url = reverse('hris:login')
        self.assertEqual(resolve(url).func, views.loginUser)

    def test_logout_url_resolves(self):
        url = reverse('hris:logout')
        self.assertEqual(resolve(url).func, views.logout_user)

    def test_registration_url_resolves(self):
        url = reverse('hris:registration')
        self.assertEqual(resolve(url).func, views.registration)

    def test_doLogin_url_resolves(self):
        url = reverse('hris:doLogin')
        self.assertEqual(resolve(url).func, views.doLogin)

    def test_doRegistration_url_resolves(self):
        url = reverse('hris:doRegistration')
        self.assertEqual(resolve(url).func, views.doRegistration)

    def test_batch_add_url_resolves(self):
        url = reverse('hris:batch-add')
        self.assertEqual(resolve(url).func, views.add_accounts)

    def test_add_account_url_resolves(self):
        url = reverse('hris:add-account')
        self.assertEqual(resolve(url).func, views.add_account)

    def test_reset_account_url_resolves(self):
        url = reverse('hris:reset-account', args=['1'])
        self.assertEqual(resolve(url).func, views.reset_account)
