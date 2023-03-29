
from django.test import TestCase, Client
from django.urls import reverse
from staff_app.models import Employee, Contacts, Publications, Requests, Presentations, Conferences, Awards, Honours, Contributions
from hris_app.models import CustomUser


class TestAdminViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_superuser(
            username='testuser',
            email='testuser@gmail.com',
            first_name='Test',
            last_name='User',
            password='password123',
            user_type='1'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            firstname='Test Department',
            lastname='Test Job Title'
        )
        self.year = '2021'
        self.publication = Publications.objects.create(
            user=self.user,
            title='Test Publication',
            year=self.year
        )
        self.presentation = Presentations.objects.create(
            user=self.user,
            title='Test Presentation',
            year=self.year
        )
        self.conference = Conferences.objects.create(
            user=self.user,
            title='Test Conference',
            year=self.year
        )
        self.award = Awards.objects.create(
            user=self.user,
            title='Test Award',
            year=self.year
        )
        self.honour = Honours.objects.create(
            user=self.user,
            title='Test Honour',
            year=self.year
        )
        self.contribution = Contributions.objects.create(
            user=self.user,
            contribution='Test Contribution',
            year=self.year
        )
        self.annualreports_url = reverse('admin_app:annualreports')

        self.contacts_url = reverse('admin_app:contacts')
        self.contact = Contacts.objects.create(
            name='Test Contact',
            email='test@sta.uwi.edu',
            information='test information'
        )
        self.contacts_create_url = reverse('admin_app:contact-add')
        self.contacts_edit_url = reverse(
            'admin_app:contact-edit', args=[self.contact.id])
        self.contacts_delete_url = reverse(
            'admin_app:contact-delete', args=[self.contact.id])

    def test_home_view(self):
        url = reverse('admin_app:admin-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_home.html')

    def test_employees_view(self):
        url = reverse('admin_app:employees')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/view_employees.html')

    def test_employee_info_view(self):
        employee = Employee.objects.create(firstname='John', lastname='Doe')
        url = reverse('admin_app:info', args=[employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/employee_info.html')

    def test_requests_view(self):
        url = reverse('admin_app:requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/rfi_view.html')

    def test_request_delete_view(self):
        request = Requests.objects.create()
        url = reverse('admin_app:request-delete', args=[request.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='password123')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_app:requests'))
        self.assertFalse(Requests.objects.filter(id=request.id).exists())

    def test_contacts_view_authenticated_superuser(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.contacts_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_contacts.html')

    def test_contacts_view_not_authenticated(self):
        response = self.client.get(self.contacts_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_contact_create_view_authenticated_superuser(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.contacts_create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_edit.html')

    def test_contact_create_view_not_authenticated(self):
        response = self.client.get(self.contacts_create_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_contact_add_valid_form(self):
        self.client.login(username='testuser', password='password123')

        response = self.client.post(self.contacts_create_url, {
            'name': 'Test Contact 2',
            'email': 'test2@sta.uwi.edu',
            'information': 'info 2'
        })
        contact = Contacts.objects.get(email='test2@sta.uwi.edu')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/admin_view/contacts/')
        self.assertTrue(contact)

    def test_contact_add_invalid_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.contacts_create_url, {})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_edit.html')

    def test_contact_edit_view_authenticated_superuser(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.contacts_edit_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_edit.html')

    def test_contact_edit_view_not_authenticated(self):
        response = self.client.get(self.contacts_edit_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_contact_edit_valid_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.contacts_edit_url, {
            'name': 'Test Contact Edited',
            'email': 'test_edit@sta.uwi.edu',
            'information': 'info edited'
        })
        contact = Contacts.objects.get(name='Test Contact Edited')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/admin_view/contacts/')
        self.assertTrue(contact)

    def test_contact_edit_invalid_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.contacts_edit_url, {})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_edit.html')

    def test_contact_delete(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.contacts_delete_url)
        contact = Contacts.objects.filter(name='Test Contact').first()
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/admin_view/contacts/')
        self.assertFalse(contact)

    def test_annualreports_view_authenticated_superuser(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.annualreports_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/annualreports.html')

    def test_annualreports_view_not_authenticated(self):
        response = self.client.get(self.annualreports_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')
