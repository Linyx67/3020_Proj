from django.shortcuts import (
    render,
    redirect,
    HttpResponseRedirect,
    HttpResponse
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
from staff_app.models import Employee
# Create your views here.


def home(request):
    return render(request, 'hris/home.html')


def contact(request):
    return render(request, 'contact.html')


def loginUser(request):
    return render(request, 'hris/login.html')


def doLogin(request):
    # Get email and password from POST request
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    # Check if both email and password are available
    if not (email_id and password):
        messages.error(request, "Please provide all the login details.")
        return render(request, 'hris/login.html')

    # Retrieve user from database based on email
    user = CustomUser.objects.filter(email=email_id).last()

    # If no user found, return error message and redirect to login page
    if not user:
        messages.error(request, 'Invalid Login Credentials')
        return render(request, 'hris/login.html')

    # Authenticate user based on email and password
    if not authenticate(request, username=email_id, password=password):
        messages.error(request, 'Invalid Login Credentials')
        return render(request, 'hris/login.html')

    # Log in the user
    login(request, user)

    # Redirect user to respective dashboard based on user type
    if user.user_type == CustomUser.ADMINISTRATOR:
        return redirect('admin_view/')
    elif user.user_type == CustomUser.STAFF:
        return redirect('staff_view/')

    # If user doesn't have a user_type, display home page
    return render(request, 'hris/home.html')


def registration(request):
    return render(request, 'hris/registration.html')


def doRegistration(request):
    # Extract user registration information from POST request
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirmPassword')

    # Check if all fields have been filled
    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the information')
        return render(request, 'hris/registration.html')

    # Check if password and confirm password fields match
    if password != confirm_password:
        messages.error(request, 'Please ensure that the passwords match.')
        return render(request, 'hris/registration.html')

    # Check if user with provided email already exists
    user_exists = CustomUser.objects.filter(email=email_id).exists()
    if user_exists:
        messages.error(request, 'User with this email already exists')
        return render(request, 'hris/registration.html')

    # Check if email has a valid format and determine the user type
    user_type = get_user_type_from_email(email_id)
    if user_type is None:
        messages.error(
            request, "Please use valid format for the email id: '<firstname>.<lastname>@<sta.uwi.edu>'")
        return render(request, 'hris/registration.html')

    # Create a unique username from the email
    username = email_id

    # Check if username already exists
    if CustomUser.objects.filter(username=username).exists():
        messages.error(
            request, 'User with this name already exists. Please use different username.')
        return render(request, 'hris/registration.html')

    # Create user object and save to database
    user = CustomUser()
    user.username = username
    user.email = email_id
    user.password = make_password(password)
    user.user_type = user_type
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    # Create associated objects based on user type
    if user_type == CustomUser.STAFF:
        StaffUser.objects.create(admin=user)
        employee = Employee.objects.create(user_id=user.id)
        employee.firstname = first_name
        employee.lastname = last_name
        employee.email = email_id
        employee.save()
    elif user_type == CustomUser.ADMINISTRATOR:
        AdminUser.objects.create(admin=user)

    # Render login page
    return render(request, 'hris/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

# function to batch add staff accounts using a txt file


def add_accounts(request):
    # check if user is authenticated and is a superuser
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # initialize lists to store failed and existing email addresses
    failed = []
    exists = []
    if failed:
        print("working")
    # if file is uploaded
    if request.method == 'POST':
        # checks if file is a txt file
        if not request.FILES['file'].name.endswith('.txt'):
            messages.error(request, 'Please upload a .txt file')
            return render(request, 'hris/batch_add.html')
        # read the uploaded file
        file = request.FILES['file'].read()

        # split the file into lines
        emails = file.splitlines()

        # for each email address
        for email_b in emails:
            # decode bytes to string
            email = email_b.decode("utf-8")

            # if email does not end with "sta.uwi.edu", add it to failed list
            if not email.endswith("sta.uwi.edu"):
                failed.append(email)
                continue

            # check if user already exists in the database
            user_exists = CustomUser.objects.filter(email=email).exists()
            if user_exists:
                exists.append(email)
                continue

            # create new user with default password "password"
            name = email.split('@')[0]
            first = name.split('.')[0]
            firstname = ''.join([i for i in first if not i.isdigit()])
            last = name.split('.')[1]
            lastname = ''.join([i for i in last if not i.isdigit()])
            user = CustomUser()
            user_type = get_user_type_from_email(email)
            user.username = email
            user.email = email
            user.password = make_password('password')  # default passowrd
            user.user_type = user_type
            user.first_name = firstname.capitalize()
            user.last_name = lastname.capitalize()
            user.save()
            StaffUser.objects.create(admin=user)

            # create new employee and save to database
            employee = Employee.objects.create(user_id=user.id)
            employee.firstname = firstname.capitalize()
            employee.lastname = lastname.capitalize()
            employee.email = email
            employee.save()
        # if any email failed or already exists an error message will be displayed
        if failed or exists:
            messages.error(
                request, "Failed to create the following accounts because the email address is invalid or the user already exists")
            for fail in failed:
                messages.error(request, fail)
            for exist in exists:
                messages.error(request, exist)
        else:
            messages.success(request, "All Accounts successfully created")
    # create dictionary to store lists of failed and existing email addresses and return to the user interface
    context = {
        "failed": failed,
        "exists": exists
    }
    return render(request, "hris/batch_add.html", context)

# function to render add accounts page


def add_account_view(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    return render(request, "hris/add_account.html")

# function to add a new staff account by entering email address


def add_account(request):
    # Only authenticated superusers can add accounts
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get the email address from the request
    email = request.POST.get('email_address')

    # Check if a user with this email address already exists
    user_exists = CustomUser.objects.filter(email=email).exists()
    if user_exists:
        # If a user already exists with this email address, display an error message and render the page again
        messages.error(request, 'User with this email already exists')
        return render(request, 'hris/add_account.html')
    elif not email.endswith('@sta.uwi.edu'):
        messages.error(request, 'Invalid email address')
        return render(request, 'hris/add_account.html')
    else:
        # If a user does not exist with this email address, create a new user with default password
        name = email.split('@')[0]
        first = name.split('.')[0]
        firstname = ''.join([i for i in first if not i.isdigit()])
        last = name.split('.')[1]
        lastname = ''.join([i for i in last if not i.isdigit()])
        user = CustomUser()
        user_type = get_user_type_from_email(email)
        user.username = email
        user.email = email
        user.password = make_password('password')  # default passowrd
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

        # Display a success message and render the page again
        messages.success(request, 'Successfully added user')
        return render(request, "hris/add_account.html")

    # This return statement is unreachable because it's after the "return render" statement
    return render(request, "hris/add_account.html")


def reset_account(request, id):
    return redirect('admin_app:home')


def reset_accounts(request, id):
    return redirect('admin_app:home')


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
