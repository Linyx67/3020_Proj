
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from hris_app.models import CustomUser
from staff_app.models import Employee
from hris_app.views import doLogin


class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('hris:doLogin')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            first_name='Test',
            last_name='User',
            password='password123',
            user_type='2'
        )
        self.user_info = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'j.doe@sta.uwi.edu',
            'password': 'password',
            'confirmPassword': 'password',
        }
        self.invalid_email = 'invalid.email.com'

        self.registration_url = reverse('hris:doRegistration')

    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hris/login.html')

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertTrue(
            CustomUser.objects.get(
                username='testuser').is_authenticated
        )

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertContains(response, 'Invalid Login Credentials')
        self.assertTemplateUsed(response, 'hris/login.html')

    def test_successful_registration(self):
        response = self.client.post(
            self.registration_url,
            data=self.user_info
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hris/login.html')

        # Check if user and employee objects were created successfully
        user = CustomUser.objects.get(email=self.user_info['email'])
        employee = Employee.objects.get(user_id=user.id)
        self.assertEqual(user.first_name, self.user_info['first_name'])
        self.assertEqual(user.last_name, self.user_info['last_name'])
        self.assertEqual(user.email, self.user_info['email'])
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.user_type)
        self.assertEqual(employee.firstname, self.user_info['first_name'])
        self.assertEqual(employee.lastname, self.user_info['last_name'])
        self.assertEqual(employee.email, self.user_info['email'])

    def test_missing_information(self):
        for field in ['email', 'password', 'confirmPassword']:
            info_copy = self.user_info.copy()
            del info_copy[field]
            response = self.client.post(
                self.registration_url,
                data=info_copy
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Please provide all the information')
            self.assertTemplateUsed(response, 'hris/registration.html')

    def test_password_mismatch(self):
        info_copy = self.user_info.copy()
        info_copy['password'] = 'incorrect_password'
        response = self.client.post(
            self.registration_url,
            data=info_copy
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Please ensure that the passwords match.')
        self.assertTemplateUsed(response, 'hris/registration.html')

    def test_add_account_authenticated_superuser(self):
        # Create a superuser for authentication
        self.user1 = CustomUser.objects.create_superuser(
            username='testuser1',
            email='testuser@sta.uwi.edu',
            password='test1234',
            user_type='1'
        )
        self.client.login(username='testuser1', password='test1234')

        response = self.client.post(reverse('hris:add-account'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'johndoe@sta.uwi.edu',
            'type': 'staff'
        })

        # Check if the response redirects to the add account page
        self.assertEqual(response.status_code, 302)

        # Check if the user account was created
        self.assertTrue(CustomUser.objects.filter(
            email='johndoe@sta.uwi.edu').exists())
        self.assertTrue(Employee.objects.filter(
            email='johndoe@sta.uwi.edu').exists())

    # Test if unauthenticated users can't add accounts
    def test_add_account_unauthenticated_user(self):
        response = self.client.post(reverse('hris:add-account'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'johndoe@sta.uwi.edu',
            'type': '1'
        })

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('hris:home'))

    # Test if accounts with duplicate email addresses can't be created
    def test_add_account_duplicate_email(self):
        # Create a user with the email 'johndoe@sta.uwi.edu'
        user = CustomUser.objects.create(
            username='johndoe@sta.uwi.edu',
            email='johndoe@sta.uwi.edu',
            password=make_password('password'),  # default password
            user_type='2',
            first_name='John',
            last_name='Doe'
        )
        employee = Employee.objects.create(user=user)

        # Try to create another account with the same email
        response = self.client.post(reverse('hris:add-account'), {
            'firstname': 'Jane',
            'lastname': 'Doe',
            'email': 'johndoe@sta.uwi.edu',
            'type': '2'
        })

        # Check if the response redirects to the add account page
        self.assertEqual(response.status_code, 302)

    # Test if invalid email addresses can't be used to create accounts

    def test_add_account_invalid_email(self):
        response = self.client.post(reverse('hris:add-account'), {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'johndoe@gmail.com',
            'type': '2'
        })

        # Check if the response redirects to the add account page
        self.assertEqual(response.status_code, 302)
