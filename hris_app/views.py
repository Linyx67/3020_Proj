from django.shortcuts import (
    render,
    HttpResponse,
    redirect,
    HttpResponseRedirect,
)
from django.contrib.auth import (
    logout,
    authenticate,
    login
)
from .models import (
    CustomUser,
    AdminUser,
    StaffUser
)
from django.contrib import messages
from staff_app import views
# Create your views here.


def home(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')


def loginUser(request):
    return render(request, 'login_page.html')


def doLogin(request):
    print("here")
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    print(email_id)
    print(password)
    print(request.user)
    if not (email_id and password):
        messages.error(request, "Please provide all the login details.")
        return render(request, 'login_page.html')

    user = CustomUser.objects.filter(email=email_id, password=password).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials')
        return render(request, 'login_page.html')

    login(request, user)
    print(request, user)  # for testing

    if user.user_type == CustomUser.ADMINISTRATOR:
        return redirect('admin_view/')
    elif user.user_type == CustomUser.STAFF:
        return redirect('staff_view/')

    return render(request, 'home.html')


def registration(request):
    return render(request, 'registration.html')


def doRegistration(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirmPassword')

    print(email_id)  # for testing
    print(password)
    print(confirm_password)
    print(first_name)
    print(last_name)

    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the information')
        return render(request, 'registration.html')

    if password != confirm_password:
        messages.error(request, 'Please ensure that the passowrds match.')
        return render(request, 'registration.html')

    user_exists = CustomUser.objects.filter(email=email_id).exists()
    if user_exists:
        messages.error(request, 'User with this email already exists')
        return render(request, 'registration.html')

    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(
            request, "Please use valid format for the email id: '<firstname>.<lastname>@<sta.uwi.edu>'")
        return render(request, 'registration.html')

    username = email_id
    print(username)
    if CustomUser.objects.filter(username=username).exists():
        messages.error(
            request, 'User with this name already exists. Please use different username.')
        return render(request, 'registration.html')

    user = CustomUser()
    user.username = username
    user.email = email_id
    user.password = password
    user.user_type = user_type
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    if user_type == CustomUser.STAFF:
        StaffUser.objects.create(admin=user)
    elif user_type == CustomUser.ADMINISTRATOR:
        AdminUser.objects.create(admin=user)
    return render(request, 'login_page.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def get_user_type_from_email(email_id):
    # """
    # Returns CustomUser.user_type corresponding to the given email address
    # email_id should be in following format:
    # '<username>.<staff|student|hod>@<college_domain>'
    # eg.: 'abhishek.staff@jecrc.com'
    # """

    try:
        email_id = email_id.split('@')[0]
        email_user_type = 'staff'  # email_id.split('.')[1]
        return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
    except:
        return None
