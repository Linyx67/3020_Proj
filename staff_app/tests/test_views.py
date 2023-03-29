from django.test import TestCase, Client
from django.urls import reverse
from hris_app.models import CustomUser
from staff_app.models import Employee
from staff_app.forms import EmployeeCreateForm
from staff_app.views import *
from django.contrib.auth.hashers import make_password


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            first_name='Test',
            last_name='User',
            password='testpassword',
            user_type='2'
        )
        self.home_url = reverse('staff:staff-home')
        self.profile_url = reverse('staff:profile')
        self.profile_update_url = reverse('staff:profile-update')
        self.add_award_url = reverse('staff:award-add')
        self.edit_award_url = reverse('staff:award-edit', args=[1])
        self.delete_award_url = reverse('staff:award-delete', args=[1])
        self.view_awards_url = reverse('staff:award')

        self.employee = Employee.objects.create(
            user=self.user, firstname='Test', lastname='User')
        self.form_data = {
            'firstname': 'New Test Employee',
            'lastname': 'Tester II',
            'bio': 'This is test bio',
        }
        self.consultancy = Consultancies.objects.create(
            user=self.user,
            title='Test Consultancy',
            period='2022-12-31',
            position='Test position')

    def test_home_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('staff:staff-home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('hris:home'))

    def test_home_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('staff:staff-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_home.html')

    def test_profile_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('staff:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('hris:home'))

    def test_profile_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('staff:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_profile.html')
        self.assertContains(response, 'Test')

    def test_authenticated_user_can_update_profile(self):
        self.user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='testuser@sta.uwi.edu',
            first_name='Test',
            last_name='User',
            password='testpassword',
            user_type='2'
        )
        self.employee1 = Employee.objects.create(
            user=self.user1, firstname='Test', lastname='User', email='test@sta.uwi.edu', othername='Testtest')
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('staff:profile-update'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EmployeeCreateForm)

        response = self.client.post(reverse('staff:profile-update'), {
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@sta.uwi.edu',
            'othername': 'Testtest',
        })
        self.assertEqual(response.status_code, 200)

        self.assertTrue(Employee.objects.filter(user=self.user1).exists())
        employee = Employee.objects.get(user=self.user1)
        self.assertEqual(employee.firstname, 'Test')
        self.assertEqual(employee.lastname, 'User')
        self.assertEqual(employee.email, 'test@sta.uwi.edu')
        self.assertEqual(employee.othername, 'Testtest')

    def test_unauthenticated_user_cannot_update_profile(self):
        response = self.client.get(reverse('staff:profile-update'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('hris:home'))

        response = self.client.post(reverse('staff:profile-update'), {
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@test.com',
            'tel': '1234567890',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('hris:home'))

    def test_consultancy_add(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Create a POST request
        response = self.client.post(reverse('staff:consultancy-add'),
                                    {'title': 'New Test Consultancy',
                                    'period': '2022-12-31',
                                     'position': 'New Test position'})

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the consultancy is created successfully
        self.assertEqual(Consultancies.objects.all().count(), 2)

    def test_consultancy_edit(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Create a POST request
        response = self.client.post(reverse('staff:consultancy-edit',
                                    args=[self.consultancy.id]),
                                    {'title': 'Updated Test Consultancy',
                                    'period': '2022-12-31',
                                     'position': 'Updated Test position'})

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the consultancy is updated successfully
        consultancy = Consultancies.objects.get(id=self.consultancy.id)
        self.assertEqual(consultancy.title, 'Updated Test Consultancy')

    def test_consultancy_delete(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Create a POST request
        response = self.client.post(reverse('staff:consultancy-delete',
                                    args=[self.consultancy.id]))

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the consultancy is deleted successfully
        self.assertEqual(Consultancies.objects.all().count(), 0)
