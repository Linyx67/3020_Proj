
from django.urls import resolve, reverse
from django.test import SimpleTestCase
from admin_app import views


class TestUrls(SimpleTestCase):

    def test_admin_home_url(self):
        url = reverse('admin_app:admin-home')
        self.assertEqual(resolve(url).func, views.home)

    def test_employees_url(self):
        url = reverse('admin_app:employees')
        self.assertEqual(resolve(url).func, views.employees)

    def test_download_vitae_url(self):
        url = reverse('admin_app:download', args=[10])
        self.assertEqual(resolve(url).func, views.download_vitae)

    def test_employees_info_url(self):
        url = reverse('admin_app:info', args=[10])
        self.assertEqual(resolve(url).func, views.employees_info)

    def test_publications_url(self):
        url = reverse('admin_app:publications')
        self.assertEqual(resolve(url).func, views.publications)

    def test_pubs_journals_url(self):
        url = reverse('admin_app:pubs-journals')
        self.assertEqual(resolve(url).func, views.pubs_journals)

    def test_pubs_papers_url(self):
        url = reverse('admin_app:pubs-papers')
        self.assertEqual(resolve(url).func, views.pubs_papers)

    def test_pubs_books_url(self):
        url = reverse('admin_app:pubs-books')
        self.assertEqual(resolve(url).func, views.pubs_books)

    def test_contacts_view_url(self):
        url = reverse('admin_app:contacts')
        self.assertEqual(resolve(url).func, views.contacts_view)

    def test_contact_add_url(self):
        url = reverse('admin_app:contact-add')
        self.assertEqual(resolve(url).func, views.contact_add)

    def test_contact_edit_url(self):
        url = reverse('admin_app:contact-edit', args=[10])
        self.assertEqual(resolve(url).func, views.contact_edit)

    def test_contact_delete_url(self):
        url = reverse('admin_app:contact-delete', args=[10])
        self.assertEqual(resolve(url).func, views.contact_delete)

    def test_requests_view_url(self):
        url = reverse('admin_app:requests')
        self.assertEqual(resolve(url).func, views.requests_view)

    def test_request_delete_url(self):
        url = reverse('admin_app:request-delete', args=[10])
        self.assertEqual(resolve(url).func, views.request_delete)

    def test_annualreports_url(self):
        url = reverse('admin_app:annualreports')
        self.assertEqual(resolve(url).func, views.annualreports)

    def test_annualreport_pdf_url(self):
        url = reverse('admin_app:annualreport-pdf', args=[10])
        self.assertEqual(resolve(url).func, views.annualreport_pdf)
