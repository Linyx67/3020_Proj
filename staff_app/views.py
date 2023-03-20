from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from hris_app.models import StaffUser, CustomUser
from django.db.models import Q
from .models import Employee, Publications, Awards, Leave
from .functions import get_user_info
from .forms import (
    AwardsCreateForm,
    PublicationsCreateForm,
    EmployeeCreateForm,
    LeaveCreateForm
)
# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return redirect('hris:home')
    return render(request, 'staff/staff_home.html')


def profile(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')
    # Get the user information from the database
    dataset = get_user_info(request.user.id)
    # Render the staff_profile.html template and pass the user information to it
    return render(request, "staff/staff_profile.html", dataset)


def profile_update(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Check if an Employee object exists for the user
    if Employee.objects.filter(user_id=request.user.id).exists():
        # If an Employee object exists, get it and prepopulate the form with its data
        employee = get_object_or_404(Employee, user_id=request.user.id)
        form = EmployeeCreateForm(
            request.POST or None, request.FILES or None, instance=employee)
    else:
        # If an Employee object does not exist, create a new, empty form
        form = EmployeeCreateForm()

    # If the form has been submitted and is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        # Redirect to the profile view
        return redirect('/staff_view/profile/')

    # Pass the form to the template for rendering
    context = {
        'form': form
    }
    return render(request, "staff/staff_profile_edit.html", context)


def add_award(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Create an instance of the AwardsCreateForm form class
    form = AwardsCreateForm(request.POST or None)

    # If the form has been submitted and is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        # Redirect to the awards view
        return redirect('/staff_view/awards/')

    # Pass the form to the template for rendering
    context = {
        'form': form
    }
    return render(request, "staff/staff_awards_edit.html", context)


def edit_award(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the award object with the specified id, or raise a 404 error if it doesn't exist
    awards = get_object_or_404(Awards, id=id)

    # Create a form instance with the retrieved awards object
    form = AwardsCreateForm(request.POST or None, instance=awards)

    # If the form has been submitted and is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        # Redirect to the awards view
        return redirect('/staff_view/awards/')

    # Pass the form to the template for rendering
    context = {
        'form': form
    }
    return render(request, "staff/staff_awards_edit.html", context)


def view_awards(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Check if there are any awards associated with the current user
    if Awards.objects.filter(user_id=request.user.id).exists():
        # If there are awards, retrieve them from the database
        awards = Awards.objects.filter(user_id=request.user.id)
    else:
        # If there are no awards, create an empty list
        awards = []

    # Pass the list of awards to the template for rendering
    context = {
        "object": awards
    }
    return render(request, 'staff/staff_awards.html', context)


def add_publication(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Create a new instance of the PublicationsCreateForm
    form = PublicationsCreateForm(request.POST or None)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()

        # Redirect to the publications page
        return redirect('/staff_view/publications/')

    # If the form is not valid, render the staff_publications_edit template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_publications_edit.html", context)


def edit_publication(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the publication object with the specified id
    publications = get_object_or_404(Publications, id=id)

    # Create a new instance of the PublicationsCreateForm, passing in the publication object as an instance
    form = PublicationsCreateForm(request.POST or None, instance=publications)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()

        # Redirect to the publications page
        return redirect('/staff_view/publications/')

    # If the form is not valid, render the staff_publications_edit template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_publications_edit.html", context)


def view_publications(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not, redirect to the home page
        return redirect('hris:home')

    # Check if the logged-in user has any publications
    if Publications.objects.filter(user_id=request.user.id).exists():
        # If there are publications, retrieve them and store them in the "publications" variable
        publications = Publications.objects.filter(user_id=request.user.id)
    else:
        # If there are no publications, store an empty list in the "publications" variable
        publications = []

    # Pass the "publications" variable to the "staff/staff_publications.html" template as "object"
    context = {
        "object": publications
    }
    return render(request, "staff/staff_publications.html", context)


def add_leave(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a LeaveCreateForm object based on the request's POST data
    form = LeaveCreateForm(request.POST or None)

    # If form is valid, save the leave request and redirect to the staff view page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        return redirect('/staff_view/')

    # If form is not valid, render the staff_leave_add template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_leave_add.html", context)


def view_leave(request):
    # Redirect unauthenticated users to the home page
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Get all leave records for the current user
    if Leave.objects.filter(user_id=request.user.id).exists():
        leave = Leave.objects.filter(user_id=request.user.id)
    else:
        leave = []

    # Pass leave records to the template
    context = {
        "object": leave
    }
    return render(request, "staff/staff_leave_view.html", context)
