from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'hris'

urlpatterns = [

    path('', views.home, name="home"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
    path('batch_add/', views.add_accounts, name="batch-add"),
    path('add_account/', views.add_account, name="add-account"),
    path('reset_account/<int:id>/', views.reset_account, name="reset-account"),

    # Django built in password change and reset functions
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done"),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),

]
