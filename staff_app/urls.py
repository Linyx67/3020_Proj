from django.urls import path, include
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.home, name="staff-home"),
    path('profile/', views.profile, name="profile"),
    path('profile_update/', views.profile_update, name="profile-update"),
    path('apply_leave/', views.apply_leave, name="apply-leave"),
    path('apply_leave_save/', views.apply_leave_save, name="apply-leave-save"),
    path('awards/', views.view_awards, name="award"),
    path('publications/', views.view_publications, name="publication"),
    path('awards_edit/', views.edit_award, name="award-edit"),
    path('publications_edit/', views.edit_publication, name="publication-edit"),

]
