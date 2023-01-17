from django.urls import path, include
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('', views.home, name="admin-home"),
    path('employees/', views.employees, name="employees"),
    path('leaves/', views.leaves_list, name="leaves"),
]
