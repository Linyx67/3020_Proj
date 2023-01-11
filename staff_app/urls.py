from django.urls import path, include
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.home, name="staff-home"),
    path('profile', views.profile, name="profile"),
    path('profile_update', views.profile_update, name="profile-update"),
    path('apply_leave', views.apply_leave, name="apply-leave"),
    path('apply_leave_save', views.apply_leave_save, name="apply-leave-save"),
    path('Awards', views.add_award, name="award"),
    path('Publications', views.add_publication, name="publication"),

]
