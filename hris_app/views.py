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
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from staff_app import views
from staff_app.models import Employee
# Create your views here.


def home(request):
    return render(request, 'hris/home.html')


def contact(request):
    return render(request, 'contact.html')


def loginUser(request):
    return render(request, 'hris/login.html')


def doLogin(request):
    print("here")
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    print(email_id)
    print(password)
    print(request.user)
    if not (email_id and password):
        messages.error(request, "Please provide all the login details.")
        return render(request, 'hris/login.html')

    user = CustomUser.objects.filter(email=email_id).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials')
        return render(request, 'hris/login.html')
    if not authenticate(request, username=email_id, password=password):
        messages.error(request, 'Invalid Login Credentials')
        return render(request, 'hris/login.html')
    login(request, user)
    print(request, user)  # for testing

    if user.user_type == CustomUser.ADMINISTRATOR:
        return redirect('admin_view/')
    elif user.user_type == CustomUser.STAFF:
        return redirect('staff_view/')

    return render(request, 'hris/home.html')


def registration(request):
    return render(request, 'hris/registration.html')


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
        return render(request, 'hris/registration.html')

    if password != confirm_password:
        messages.error(request, 'Please ensure that the passowrds match.')
        return render(request, 'hris/registration.html')

    user_exists = CustomUser.objects.filter(email=email_id).exists()
    if user_exists:
        messages.error(request, 'User with this email already exists')
        return render(request, 'hris/registration.html')

    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(
            request, "Please use valid format for the email id: '<firstname>.<lastname>@<sta.uwi.edu>'")
        return render(request, 'hris/registration.html')

    username = email_id
    print(username)
    if CustomUser.objects.filter(username=username).exists():
        messages.error(
            request, 'User with this name already exists. Please use different username.')
        return render(request, 'hris/registration.html')

    user = CustomUser()
    user.username = username
    user.email = email_id
    user.password = make_password(password)
    user.user_type = user_type
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    if user_type == CustomUser.STAFF:
        StaffUser.objects.create(admin=user)
        employee = Employee.objects.create(user_id=user.id)
        employee.firstname = first_name
        employee.lastname = last_name
        employee.email = email_id
        employee.save()
    elif user_type == CustomUser.ADMINISTRATOR:
        AdminUser.objects.create(admin=user)
    return render(request, 'hris/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def add_accounts(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    if request.FILES:
        file = request.FILES['file'].read()
        emails = file.splitlines()
        for email_b in emails:
            email = email_b.decode("utf-8")
            name = email.split('@')[0]
            firstname = name.split('.')[0]
            last = name.split('.')[1]
            lastname = ''.join([i for i in last if not i.isdigit()])
            user = CustomUser()
            user_type = get_user_type_from_email(email)
            user.username = email
            user.email = email
            user.password = make_password('password')
            user.user_type = user_type
            user.first_name = firstname.capitalize()
            user.last_name = lastname.capitalize()
            user.save()
            StaffUser.objects.create(admin=user)
            employee = Employee.objects.create(user_id=user.id)
            employee.firstname = firstname.capitalize()
            employee.lastname = lastname.capitalize()
            employee.email = email
            employee.save()
    return render(request, 'hris/add_accounts.html')


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
