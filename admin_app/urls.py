from django.urls import path, include
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('', views.home, name="admin-home"),
    path('employees/', views.employees, name="employees"),
    path('employee/download/<int:id>/', views.download_vitae, name="download"),
    path('employee/<int:id>/', views.employees_info, name="info"),

    path('awards/', views.awards, name="awards"),
    path('publications/', views.publications, name="publications"),
    path('publications/journals/', views.pubs_journals, name="pubs-journals"),
    path('publications/conference/', views.pubs_papers, name="pubs-papers"),
    path('publications/books/', views.pubs_books, name="pubs-books"),

    path('contacts/', views.contacts_view, name="contacts"),
    path('contacts_add/', views.contact_add, name="contact-add"),
    path('contacts_edit/<int:id>/', views.contact_edit, name="contact-edit"),
    path('contacts_delete/<int:id>/',
         views.contact_delete, name="contact-delete"),

    path('requests/', views.requests_view, name="requests"),
    path('request_delete/<int:id>/', views.request_delete, name="request-delete"),

    path('annualreports/', views.annualreports, name='annualreports'),
    path('annualreports/<int:id>/',
         views.annualreport_pdf, name='annualreport-pdf'),
]

'''
     path('leaves/all/', views.leaves_list, name="leaves"),
    path('leaves/pending/', views.leaves_pending_list, name="leaves-pending"),
    path('leaves/approved/', views.leaves_approved_list, name='leaves-approved'),
    path('leaves/cancelled/', views.cancel_leaves_list, name='leaves-cancelled'),
    path('leaves/rejected/', views.leave_rejected_list, name='leaves-rejected'),
    path('leaves/view/<int:id>/', views.leaves_view, name='leave-employee'),
    path('leaves/approve/<int:id>/', views.approve_leave, name='leave-approve'),
    path('leaves/unapprove/<int:id>/',
         views.unapprove_leave, name='leave-unapprove'),
    path('leaves/cancel/<int:id>/', views.cancel_leave, name='leave-cancel'),
    path('leaves/uncancel/<int:id>/', views.uncancel_leave, name='leave-uncancel'),
    path('leaves/reject/<int:id>/', views.reject_leave, name='leave-reject'),
    path('leaves/unreject/<int:id>/', views.unreject_leave, name='leave-unreject'),
    '''
