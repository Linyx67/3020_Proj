from django.urls import path, include
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('', views.home, name="admin-home"),
    path('employees/', views.employees, name="employees"),
    path('employee_info/<int:id>/', views.employees_info, name="info"),
    path('leaves/', views.leaves_list, name="leaves"),

]
