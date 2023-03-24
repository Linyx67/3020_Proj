from django.urls import path, include
from . import views


app_name = 'staff'

urlpatterns = [
    path('', views.home, name="staff-home"),
    path('profile/', views.profile, name="profile"),
    path('profile_update/', views.profile_update, name="profile-update"),

    path('awards/', views.view_awards, name="award"),
    path('awards_add/', views.add_award, name="award-add"),
    path('awards_edit/<int:id>/', views.edit_award, name="award-edit"),
    path('awards_delete/<int:id>/', views.delete_award, name="award-delete"),

    path('publications/', views.view_publications, name="publication"),
    path('publications_add/', views.add_publication, name="publication-add"),
    path('publications_edit/<int:id>/',
         views.edit_publication, name="publication-edit"),
    path('publications_delete/<int:id>/',
         views.publication_delete, name="publication-delete"),

    path('conference_add/', views.conferences_add, name="conference-add"),
    path('conference_edit/<int:id>/',
         views.conferences_edit, name="conference-edit"),
    path('conference_delete/<int:id>/',
         views.conferences_delete, name="conference-delete"),

    path('consultancy_add/', views.consultancies_add, name="consultancy-add"),
    path('consultancy_edit/<int:id>/',
         views.consultancies_edit, name="consultancy-edit"),
    path('consultancy_delete/<int:id>/',
         views.consultancies_delete, name="consultancy-delete"),

    path('development_add/', views.development_add, name="development-add"),
    path('development_edit/<int:id>/',
         views.development_edit, name="development-edit"),
    path('development_delete/<int:id>/',
         views.development_delete, name="development-delete"),

    path('grant_add/', views.grants_add, name="grant-add"),
    path('grant_edit/<int:id>/', views.grants_edit, name="grant-edit"),
    path('grant_delete/<int:id>/', views.grants_delete, name="grant-delete"),

    path('manuscript_add/', views.manuscripts_add, name="manuscript-add"),
    path('mauscript_edit/<int:id>/',
         views.manuscripts_edit, name="manuscript-edit"),
    path('manuscript_delete/<int:id>/',
         views.manuscripts_delete, name="manuscript-delete"),

    path('presentation_add/', views.presentations_add, name="presentation-add"),
    path('presentation_edit/<int:id>/',
         views.presentations_edit, name="presentation-edit"),
    path('presentation_delete/<int:id>/',
         views.presentations_delete, name="presentation-delete"),

    path('research_add/', views.research_add, name="research-add"),
    path('research_edit/<int:id>/', views.research_edit, name="research-edit"),
    path('research_delete/<int:id>/',
         views.research_delete, name="research-delete"),

    path('requests/', views.rfi, name="requests"),
    path('requests_add/', views.rfi_add, name="request-add"),

    path('role_add/', views.roles_add, name="role-add"),
    path('role_edit/<int:id>/', views.roles_edit, name="role-edit"),
    path('role_delete/<int:id>/', views.roles_delete, name="role-delete"),

    path('supervision_add/', views.supervision_add, name="supervision-add"),
    path('supervision_edit/<int:id>/',
         views.supervision_edit, name="supervision-edit"),
    path('supervision_delete/<int:id>/',
         views.supervision_delete, name="supervision-delete"),

    path('specialisation_add/', views.specialisation_add,
         name="specialisation-add"),
    path('specialisation_edit/<int:id>/',
         views.specialisation_edit, name="specialisation-edit"),
    path('specialisation_delete/<int:id>/',
         views.specialisation_delete, name="specialisation-delete"),

    path('leave_add/', views.add_leave, name="add-leave"),
    path('leave/', views.view_leave, name="leave"),

]
