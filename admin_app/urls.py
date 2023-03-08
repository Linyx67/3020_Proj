from django.urls import path, include
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('', views.home, name="admin-home"),
    path('employees/', views.employees, name="employees"),
    path('employee_info/<int:id>/', views.employees_info, name="info"),

    path('awards/', views.awards, name="awards"),
    path('publications/', views.publications, name="publications"),

    path('leaves/pending/', views.leaves_list, name="leaves"),
    path('leaves/approved/', views.leaves_approved_list, name='leave-approved'),
    path('leaves/cancelled/', views.cancel_leaves_list, name='leave-cancelled'),
    path('leaves/rejected/', views.leave_rejected_list, name='leave-rejected'),
    path('leaves/view/<int:id>/', views.leaves_view, name='leave-employee'),
    path('leaves/approve/<int:id>/', views.approve_leave, name='leave-approve'),
    path('leaves/unapprove/<int:id>/',
         views.unapprove_leave, name='leave-unapprove'),
    path('leaves/cancel/<int:id>/', views.cancel_leave, name='leave-cancel'),
    path('leaves/uncancel/<int:id>/', views.uncancel_leave, name='leave-uncancel'),
    path('leaves/reject/<int:id>/', views.reject_leave, name='leave-reject'),
    path('leaves/unreject/<int:id>/', views.unreject_leave, name='leave-reject'),

]
