
from django.urls import reverse, resolve
from django.test import TestCase
from . import views


class TestUrls(TestCase):

    def test_home_url_resolves(self):
        url = reverse('staff-home')
        self.assertEqual(resolve(url).func, views.home)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, views.profile)

    def test_profile_update_url_resolves(self):
        url = reverse('profile-update')
        self.assertEqual(resolve(url).func, views.profile_update)

    def test_awards_url_resolves(self):
        url = reverse('award')
        self.assertEqual(resolve(url).func, views.view_awards)

    def test_awards_add_url_resolves(self):
        url = reverse('award-add')
        self.assertEqual(resolve(url).func, views.add_award)

    def test_awards_edit_url_resolves(self):
        url = reverse('award-edit', args=[1])
        self.assertEqual(resolve(url).func, views.edit_award)

    def test_awards_delete_url_resolves(self):
        url = reverse('award-delete', args=[1])
        self.assertEqual(resolve(url).func, views.delete_award)

    def test_publications_url_resolves(self):
        url = reverse('publication')
        self.assertEqual(resolve(url).func, views.view_publications)

    def test_publications_add_url_resolves(self):
        url = reverse('publication-add')
        self.assertEqual(resolve(url).func, views.add_publication)

    def test_publications_edit_url_resolves(self):
        url = reverse('publication-edit', args=[1])
        self.assertEqual(resolve(url).func, views.edit_publication)

    def test_publications_delete_url_resolves(self):
        url = reverse('publication-delete', args=[1])
        self.assertEqual(resolve(url).func, views.publication_delete)

    def test_conferences_url_resolves(self):
        url = reverse('conference')
        self.assertEqual(resolve(url).func, views.conferences_view)

    def test_conferences_add_url_resolves(self):
        url = reverse('conference-add')
        self.assertEqual(resolve(url).func, views.conferences_add)

    def test_conferences_edit_url_resolves(self):
        url = reverse('conference-edit', args=[1])
        self.assertEqual(resolve(url).func, views.conferences_edit)

    def test_conferences_delete_url_resolves(self):
        url = reverse('conference-delete', args=[1])
        self.assertEqual(resolve(url).func, views.conferences_delete)

    def test_consultancies_url_resolves(self):
        url = reverse('consultancies')
        self.assertEqual(resolve(url).func, views.consultancies_view)

    def test_consultancies_add_url_resolves(self):
        url = reverse('consultancy-add')
        self.assertEqual(resolve(url).func, views.consultancies_add)

    def test_consultancies_edit_url_resolves(self):
        url = reverse('consultancy-edit', args=[1])
        self.assertEqual(resolve(url).func, views.consultancies_edit)

    def test_consultancies_delete_url_resolves(self):
        url = reverse('consultancy-delete', args=[1])
        self.assertEqual(resolve(url).func, views.consultancies_delete)

    def test_development_url_resolves(self):
        url = reverse('development')
        self.assertEqual(resolve(url).func, views.development_view)

    def test_development_add_url_resolves(self):
        url = reverse('development-add')
        self.assertEqual(resolve(url).func, views.development_add)

    def test_development_edit_url_resolves(self):
        url = reverse('development-edit', args=[1])
        self.assertEqual(resolve(url).func, views.development_edit)

    def test_development_delete_url_resolves(self):
        url = reverse('development-delete', args=[1])
        self.assertEqual(resolve(url).func, views.development_delete)

    def test_grants_url_resolves(self):
        url = reverse('grants')
        self.assertEqual(resolve(url).func, views.grants_view)

    def test_grants_add_url_resolves(self):
        url = reverse('grant-add')
        self.assertEqual(resolve(url).func, views.grants_add)

    def test_grants_edit_url_resolves(self):
        url = reverse('grant-edit', args=[1])
        self.assertEqual(resolve(url).func, views.grants_edit)

    def test_grants_delete_url_resolves(self):
        url = reverse('grant-delete', args=[1])
        self.assertEqual(resolve(url).func, views.grants_delete)

    def test_manuscripts_url_resolves(self):
        url = reverse('manuscripts')
        self.assertEqual(resolve(url).func, views.manuscripts_view)

    def test_manuscripts_add_url_resolves(self):
        url = reverse('manuscript-add')
        self.assertEqual(resolve(url).func, views.manuscripts_add)

    def test_manuscripts_edit_url_resolves(self):
        url = reverse('manuscript-edit', args=[1])
        self.assertEqual(resolve(url).func, views.manuscripts_edit)

    def test_manuscripts_delete_url_resolves(self):
        url = reverse('manuscript-delete', args=[1])
        self.assertEqual(resolve(url).func, views.manuscripts_delete)

    def test_presentations_url_resolves(self):
        url = reverse('presentations')
        self.assertEqual(resolve(url).func, views.presentations_view)

    def test_presentations_add_url_resolves(self):
        url = reverse('presentation-add')
        self.assertEqual(resolve(url).func, views.presentations_add)

    def test_presentations_edit_url_resolves(self):
        url = reverse('presentation-edit', args=[1])
        self.assertEqual(resolve(url).func, views.presentations_edit)

    def test_presentations_delete_url_resolves(self):
        url = reverse('presentation-delete', args=[1])
        self.assertEqual(resolve(url).func, views.presentations_delete)

    def test_research_url_resolves(self):
        url = reverse('research')
        self.assertEqual(resolve(url).func, views.research_view)

    def test_research_add_url_resolves(self):
        url = reverse('research-add')
        self.assertEqual(resolve(url).func, views.research_add)

    def test_research_edit_url_resolves(self):
        url = reverse('research-edit', args=[1])
        self.assertEqual(resolve(url).func, views.research_edit)

    def test_research_delete_url_resolves(self):
        url = reverse('research-delete', args=[1])
        self.assertEqual(resolve(url).func, views.research_delete)

    def test_requests_url_resolves(self):
        url = reverse('requests')
        self.assertEqual(resolve(url).func, views.rfi)

    def test_requests_add_url_resolves(self):
        url = reverse('request-add')
        self.assertEqual(resolve(url).func, views.rfi_add)

    def test_requests_delete_url_resolves(self):
        url = reverse('request-delete', args=[1])
        self.assertEqual(resolve(url).func, views.rfi_delete)

    def test_roles_url_resolves(self):
        url = reverse('roles')
        self.assertEqual(resolve(url).func, views.roles_view)

    def test_roles_add_url_resolves(self):
        url = reverse('role-add')
        self.assertEqual(resolve(url).func, views.roles_add)

    def test_roles_edit_url_resolves(self):
        url = reverse('role-edit', args=[1])
        self.assertEqual(resolve(url).func, views.roles_edit)

    def test_roles_delete_url_resolves(self):
        url = reverse('role-delete', args=[1])
        self.assertEqual(resolve(url).func, views.roles_delete)

    def test_supervision_url_resolves(self):
        url = reverse('supervision')
        self.assertEqual(resolve(url).func, views.supervision_view)

    def test_supervision_add_url_resolves(self):
        url = reverse('supervision-add')
        self.assertEqual(resolve(url).func, views.supervision_add)

    def test_supervision_edit_url_resolves(self):
        url = reverse('supervision-edit', args=[1])
        self.assertEqual(resolve(url).func, views.supervision_edit)

    def test_supervision_delete_url_resolves(self):
        url = reverse('supervision-delete', args=[1])
        self.assertEqual(resolve(url).func, views.supervision_delete)

    def test_specialisation_url_resolves(self):
        url = reverse('specialisation')
        self.assertEqual(resolve(url).func, views.specialisation_view)

    def test_specialisation_add_url_resolves(self):
        url = reverse('specialisation-add')
        self.assertEqual(resolve(url).func, views.specialisation_add)

    def test_specialisation_edit_url_resolves(self):
        url = reverse('specialisation-edit', args=[1])
        self.assertEqual(resolve(url).func, views.specialisation_edit)

    def test_specialisation_delete_url_resolves(self):
        url = reverse('specialisation-delete', args=[1])
        self.assertEqual(resolve(url).func, views.specialisation_delete)

    def test_activity_url_resolves(self):
        url = reverse('activity')
        self.assertEqual(resolve(url).func, views.activity_view)

    def test_activity_add_url_resolves(self):
        url = reverse('activity-add')
        self.assertEqual(resolve(url).func, views.activity_add)

    def test_activity_edit_url_resolves(self):
        url = reverse('activity-edit', args=[1])
        self.assertEqual(resolve(url).func, views.activity_edit)

    def test_activity_delete_url_resolves(self):
        url = reverse('activity-delete', args=[1])
        self.assertEqual(resolve(url).func, views.activity_delete)

    def test_honours_url_resolves(self):
        url = reverse('honours')
        self.assertEqual(resolve(url).func, views.honour_view)

    def test_honours_add_url_resolves(self):
        url = reverse('honour-add')
        self.assertEqual(resolve(url).func, views.honour_add)

    def test_honours_edit_url_resolves(self):
        url = reverse('honour-edit', args=[1])
        self.assertEqual(resolve(url).func, views.honour_edit)

    def test_honours_delete_url_resolves(self):
        url = reverse('honour-delete', args=[1])
        self.assertEqual(resolve(url).func, views.honour_delete)

    def test_contributions_url_resolves(self):
        url = reverse('contributions')
        self.assertEqual(resolve(url).func, views.contribution_view)

    def test_contributions_add_url_resolves(self):
        url = reverse('contribution-add')
        self.assertEqual(resolve(url).func, views.contribution_add)

    def test_contributions_edit_url_resolves(self):
        url = reverse('contribution-edit', args=[1])
        self.assertEqual(resolve(url).func, views.contribution_edit)

    def test_contributions_delete_url_resolves(self):
        url = reverse('contribution-delete', args=[1])
        self.assertEqual(resolve(url).func, views.contribution_delete)

    def test_contacts_url_resolves(self):
        url = reverse('contacts')
        self.assertEqual(resolve(url).func, views.contacts_view)
