from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q

from django.http import FileResponse
import io
import re
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from hris_app.models import CustomUser
from staff_app.models import (
    Employee,
    Requests,
    Awards,
    Publications,
    Conferences,
    Presentations,
    Honours,
    Contributions,
    Contacts
)
from .forms import ReportForm, ContactsCreateForm
from staff_app.functions import get_user_info


# Create your views here.


def home(request):
    # Redirect non-authenticated and non-superuser users to the home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    dataset = dict()
    employees = Employee.objects.all()
    contacts = Contacts.objects.all()
    publications = Publications.objects.all()
    requests = Requests.objects.all()
    dataset['employees'] = employees
    dataset['contacts'] = contacts
    dataset['publications'] = publications
    dataset['requests'] = requests
    # Render the admin home page template for authenticated and superuser users
    return render(request, "admin/admin_home.html", dataset)


# view function for displaying the list of employees.


def employees(request):
    # Ensure only superusers can view the employees page,
    # else redirect to home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Create an empty dictionary to store the data
    # that will be passed to the template
    dataset = dict()

    # Retrieve all employees from the database and order them by first name
    employees = Employee.objects.all().order_by('firstname')

    # Search functionality: retrieve the search query
    # from the GET request, and filter the employees accordingly
    query = request.GET.get('search')
    if query:
        # Replace any whitespace characters with "." to allow for partial matches
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        employees = employees.filter(
            Q(email__icontains=query)
        )

    # Paginate the employees list, showing 10 employees per page
    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)

    # Add the paginated employees list,
    # total number of employees, blocked employees,
    # and title to the dataset
    dataset['employee_list'] = employees_paginated
    dataset['all_employees'] = Employee.objects.all_employees()
    blocked_employees = Employee.objects.all_blocked_employees()
    dataset['blocked_employees'] = blocked_employees
    dataset['title'] = 'Employees list view'

    # Render the employees list template with the dataset as context
    return render(request, 'admin/view_employees.html', dataset)

# view function for obtaining all relevant information about an employee.


def employees_info(request, id):
    # Check if user is authenticated and has admin privileges
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get employee's information and related data from the database
    dataset = get_user_info(id)

    # Render the employee information page with the retrieved data
    return render(request, "admin/employee_info.html", dataset)


# view function for downloading a cirriculum vitae document


def download_vitae(request, id):
    # Retrieve the Employee object with the given user ID
    object = get_object_or_404(Employee, user_id=id)

    # Get the path to the employee's vitae file
    file = object.vitae.path

    # Create a FileResponse object for the file
    response = FileResponse(open(file, 'rb'))

    # Return the FileResponse object
    return response


# function for obtaining all leave requests.

# view requests list
def requests_view(request):
    # Check if user is authenticated
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    rfis = Requests.objects.all().order_by('created')

    context = {
        "object": rfis
    }
    return render(request, "admin/rfi_view.html", context)

# delete request


def request_delete(request, id):
    # Check if user is authenticated
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    rfi = get_object_or_404(Requests, id=id)
    rfi.delete()
    messages.success(request, "Deleted successfully")
    return redirect('admin_app:requests')

# Define the view function for displaying the all awards.


def awards(request):
    # Check if user is authenticated and superuser. If not, redirect to home page.
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get all awards from the database, sorted by year.
    awards = Awards.objects.prefetch_related('user').all().order_by('-year')

    # Create a dictionary to store data for rendering the template.
    dataset = dict()

    # Search functionality: Get the query from the GET request and filter the awards accordingly.
    query = request.GET.get('search')
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        awards = awards.filter(
            Q(user__username__icontains=query)
        )

    # Pagination: Get the current page from the GET request, and show 10 awards per page.
    paginator = Paginator(awards, 10)

    # Get the current page of awards.
    page = request.GET.get('page')
    awards_paginated = paginator.get_page(page)

    # Add the paginated awards and all awards to the dataset dictionary.
    dataset['awards_list'] = awards_paginated
    dataset['all_awards'] = Awards.objects.all()

    # Add the page title to the dataset dictionary.
    dataset['title'] = 'Awards list view'

    # Render the awards template with the dataset.
    return render(request, "admin/awards.html", dataset)


# Define the view function for displaying the all publications.
def publications(request):
    # Check if the user is authenticated and a superuser, otherwise redirect to home
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get all publications, ordered by year, with related user objects pre-fetched to avoid extra database queries
    publications = Publications.objects.prefetch_related('user').all().order_by(
        '-year')

    # Create a dictionary to hold the data to be passed to the template
    dataset = dict()

    # Get the search query from the GET parameters
    query = request.GET.get('search')
    if query:
        # If the query exists, replace whitespace with periods to allow for partial matches
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        # Filter the publications queryset by matching the query against the related user's username
        publications = publications.filter(
            Q(user__username__icontains=query)
        )

    # Create a paginator object to split the publications into pages, with 10 publications per page
    paginator = Paginator(publications, 10)

    # Get the current page number from the GET parameters
    page = request.GET.get('page')
    # Get the publications for the current page
    publications_paginated = paginator.get_page(page)

    # Add the publications queryset for the current page to the dataset dictionary
    dataset['pubs_list'] = publications_paginated
    # Add the full publications queryset to the dataset dictionary
    dataset['all_pubs'] = Publications.objects.all()

    # Set the title and count title for the page
    dataset['title'] = 'Employee | Publications'
    dataset['count_title'] = 'Total Publications'

    # Render the publications view template with the dataset dictionary as the context
    return render(request, "admin/publications_view.html", dataset)


# Define the view function for displaying the journal papers.
def pubs_journals(request):
    # check if the user is authenticated and a superuser
    if not (request.user.is_authenticated and request.user.is_superuser):
        # redirect to home if the user is not authenticated or not a superuser
        return redirect('hris:home')

    # get all journal publications with related user objects and order them by year
    journals = Publications.objects.journals().prefetch_related('user').all().order_by(
        '-year')

    # create a dictionary to hold the data to be displayed on the page
    dataset = dict()
    # add all publications to the dictionary
    dataset['all_pubs'] = journals

    # get the search query from the request
    query = request.GET.get('search')
    # fix the query as the count gets reset when a query happens
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        # filter the publications based on the query
        journals = journals.filter(
            Q(user__username__icontains=query)
        )

    # create a paginator object to split the publications into pages with 10 items per page
    paginator = Paginator(journals, 10)

    # get the current page number from the request
    page = request.GET.get('page')
    # get the publications for the current page
    journals_paginated = paginator.get_page(page)

    # add the publications for the current page to the dictionary
    dataset['pubs_list'] = journals_paginated

    # add the page title and count title to the dictionary
    dataset['title'] = 'Publications | Journals'
    dataset['count_title'] = 'Total Journals'

    # render the publications view template with the dictionary
    return render(request, "admin/publications_view.html", dataset)


# Define the view function for displaying the conference papers.
def pubs_papers(request):
    # Check if the user is authenticated and is a superuser. If not, redirect to the home page.
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Retrieve all conference papers using the `papers` queryset method, and prefetch the related `user` model.
    papers = Publications.objects.papers().prefetch_related(
        'user').all().order_by('-year')

    # Initialize a dictionary to store the retrieved data.
    dataset = dict()
    dataset['all_pubs'] = papers

    # Check if there is a search query in the GET parameters.
    query = request.GET.get('search')
    # Modify the query to allow for searching using periods, then filter the papers queryset based on the query.
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        papers = papers.filter(Q(user__username__icontains=query))

    # Paginate the papers queryset, with 10 papers per page.
    paginator = Paginator(papers, 10)
    page = request.GET.get('page')
    papers_paginated = paginator.get_page(page)

    # Add the paginated papers and relevant metadata to the dataset dictionary.
    dataset['pubs_list'] = papers_paginated
    dataset['title'] = 'Publications | Conference Papers'
    dataset['count_title'] = 'Total Papers'

    # Render the publications_view template with the dataset dictionary.
    return render(request, "admin/publications_view.html", dataset)


# Define the pubs_books view function.
def pubs_books(request):
    # Check if the user is authenticated and is a superuser. If not, redirect to the home page.
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Retrieve all books using the `books` queryset method, and prefetch the related `user` model.
    books = Publications.objects.books().prefetch_related(
        'user').all().order_by('-year')

    # Initialize a dictionary to store the retrieved data.
    dataset = dict()
    dataset['all_pubs'] = books

    # Check if there is a search query in the GET parameters.
    query = request.GET.get('search')

    # Modify the query to allow for searching using periods, then filter the books queryset based on the query.
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        books = books.filter(Q(user__username__icontains=query))

    # Paginate the books queryset, with 10 books per page.
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    books_paginated = paginator.get_page(page)

    # Add the paginated books and relevant metadata to the dataset dictionary.
    dataset['pubs_list'] = books_paginated
    dataset['title'] = 'Publications | Books'
    dataset['count_title'] = 'Total Books'

    # Render the publications_view template with the dataset dictionary.
    return render(request, "admin/publications_view.html", dataset)


def contacts_view(request):
    # Check if user is authenticated
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    contacts = Contacts.objects.all()

    context = {
        "object": contacts
    }
    return render(request, "admin/admin_contacts.html", context)

# add contacts


def contact_add(request):
    # Check if user is authenticated
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Create a Contacts CreateForm object based on the request's POST data
    form = ContactsCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('admin_app:contacts')

    # If form is not valid, render the staff contacts template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit contact


def contact_edit(request, id):
    # Check if user is authenticated
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    # Get the contacts object with the specified id
    contact = get_object_or_404(Contacts, id=id)

    # Create a new instance of the Contacts create form, passing in the contacts object as an instance
    form = ContactsCreateForm(request.POST or None, instance=contact)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('admin_app:contacts')

    # If the form is not valid, render the add contacts template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete contact


def contact_delete(request, id):
    # Check if user is authenticated
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    # Get the contacts object with the specified id
    contact = get_object_or_404(Contacts, id=id)
    # Delete the contacts object
    contact.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('admin_app:contacts')


# Define the annualreports view function


def annualreports(request):
    # Check if the user is authenticated and is a superuser.
    # If not, redirect to the home page.
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Initialize an empty dictionary and create empty queryset
    # variables for the relevant models.
    dataset = dict()
    year = ''
    users = CustomUser.objects.none()
    employee = Employee.objects.none()
    journals = Publications.objects.none()
    papers = Publications.objects.none()
    books = Publications.objects.none()
    presentations = Presentations.objects.none()
    conferences = Conferences.objects.none()
    awards = Awards.objects.none()
    honours = Honours.objects.none()
    contributions = Contributions.objects.none()
    form = ReportForm(request.POST or None)
    # Check if there are any GET parameters (first_name, last_name, and year).
    if form.is_valid():
        # If there are, retrieve their values.
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        year = form.cleaned_data['year']

        # Check if a user with the given first and last names exists.
        if not CustomUser.objects.filter(first_name=firstname.capitalize(), last_name=lastname.capitalize()).exists():
            messages.error(request, 'Employee not found! Please try again.')
            return redirect('admin_app:annualreports')

        else:
            # If there is, retrieve the user object and the relevant data for that
            # user in the given year.
            users = CustomUser.objects.get(
                first_name=firstname.capitalize(), last_name=lastname.capitalize())
            employee = Employee.objects.get(user_id=users.id)
            journals = Publications.objects.journals().filter(user_id=users.id, year=year)
            papers = Publications.objects.papers().filter(user_id=users.id, year=year)
            books = Publications.objects.books().filter(user_id=users.id, year=year)
            presentations = Presentations.objects.filter(
                user_id=users.id, year=year)
            conferences = Conferences.objects.filter(
                user_id=users.id, year=year)
            awards = Awards.objects.filter(user_id=users.id, year=year)
            honours = Honours.objects.filter(user_id=users.id, year=year)
            contributions = Contributions.objects.filter(
                user_id=users.id, year=year)

    # Add the retrieved data to the dataset dictionary.
    dataset['employee'] = employee
    dataset['year'] = year
    dataset['awards'] = awards
    dataset['journals'] = journals
    dataset['papers'] = papers
    dataset['books'] = books
    dataset['presentations'] = presentations
    dataset['conferences'] = conferences
    dataset['honours'] = honours
    dataset['contributions'] = contributions
    dataset['form'] = form
    # Render the annualreports template with the dataset dictionary.
    return render(request, 'admin/annualreports.html', dataset)


def annualreport_pdf(request, id):
    # create bytestream buffer
    year = request.POST.get('year')
    buf = io.BytesIO()

    # create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # getting information for the report
    if Employee.objects.filter(user_id=id).exists():

        employee = Employee.objects.get(user_id=id)
        journals = Publications.objects.journals().filter(
            user_id=id, year=year)
        papers = Publications.objects.papers().filter(
            user_id=id, year=year)
        books = Publications.objects.books().filter(
            user_id=id, year=year)
        presentations = Presentations.objects.filter(
            user_id=id, year=year)
        conferences = Conferences.objects.filter(
            user_id=id, year=year)
        awards = Awards.objects.filter(user_id=id,  year=year)

    # lines of text
    lines = [
        "Report for Academic Year "+year,
        "===========================================================",
        " ",
        "Name: "+employee.title+' '+employee.firstname+' '+employee.lastname,
        " ",
        "===========================================================",
        "Peer Reviewed Journals Published",
        "===========================================================",
        " "
    ]
    if journals:
        for journal in journals:
            lines.append(journal.title)
    else:
        lines.append("-")

    lines.append(" ")
    lines.append(
        "===========================================================")
    lines.append("Conference Papers Published")
    lines.append(
        "===========================================================")
    lines.append(" ")

    if papers:
        for paper in papers:
            lines.append(paper.title)
    else:
        lines.append("-")

    lines.append(" ")
    lines.append(
        "===========================================================")
    lines.append("Books Published")
    lines.append(
        "===========================================================")
    lines.append(" ")

    if books:
        for book in books:
            lines.append(book.title)
    else:
        lines.append("-")

    lines.append(" ")
    lines.append(
        "===========================================================")
    lines.append("Technical Presentations")
    lines.append(
        "===========================================================")
    lines.append(" ")

    if presentations:
        for presentation in presentations:
            lines.append(presentation.title)
    else:
        lines.append("-")

    lines.append(" ")
    lines.append(
        "===========================================================")
    lines.append("Conferences Attended")
    lines.append(
        "===========================================================")
    lines.append(" ")

    if conferences:
        for con in conferences:
            lines.append(con.title)
    else:
        lines.append("-")

    lines.append(" ")
    lines.append(
        "===========================================================")
    lines.append("Awards Received")
    lines.append(
        "===========================================================")
    lines.append(" ")

    if awards:
        for award in awards:
            lines.append(award.title)
    else:
        lines.append("-")
    lines.append(" ")
    lines.append(
        "===========================================================")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    response = FileResponse(buf, as_attachment=True,
                            filename=f'{year}_{employee.firstname}_{employee.lastname}_report.pdf')

    return response


'''
def leaves_list(request):
    # check if the user is authenticated and is a superuser, else redirect to the home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # get all leaves
    leaves = Leave.objects.all()

    # create a context dictionary with the list of leaves and the page title
    context = {
        'leave_list': leaves,
        'title': 'ALL LEAVES'
    }

    # render the 'admin/leaves_view.html' template with the context dictionary
    return render(request, "admin/leaves_view.html", context)


# view function for obtaining all the pending leave requests.


def leaves_pending_list(request):
    # Check if the user is authenticated and is a superuser, otherwise redirect to home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Retrieve all pending leaves from the Leave model
    leaves = Leave.objects.all_pending_leaves()

    # Create a context dictionary containing the pending leaves and a title for the page
    context = {
        'leave_list': leaves,
        'title': 'PENDING LEAVES'
    }

    # Render the pending leaves template with the context dictionary as a parameter
    return render(request, "admin/leaves_view.html", context)


# view function for obtaining all the approved leave requests.


def leaves_approved_list(request):
    # check if the user is authenticated and a superuser
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # get all approved leaves
    leaves = Leave.objects.all_approved_leaves()

    # create context dictionary with the leave list and title
    context = {
        'leave_list': leaves,
        'title': 'approved leave list'
    }

    # render the leaves_approved template with the context
    return render(request, 'admin/leaves_approved.html', context)

# function to get all cancelled leaves.


def cancel_leaves_list(request):
    # Check if the user is authenticated and a superuser
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get all cancelled leaves
    leaves = Leave.objects.all_cancelled_leaves()

    # Create a dictionary to store data to be passed to the template
    context = {
        'leave_list_cancel': leaves,  # the cancelled leaves queryset
        'title': 'Cancel leave list'  # title for the page
    }

    # Render the template with the context dictionary
    return render(request, 'admin/leaves_cancelled.html', context)


# function to display the all the rejected leaves


def leave_rejected_list(request):
    # Check if the user is authenticated and is a superuser, otherwise redirect to home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get all rejected leave requests
    leave = Leave.objects.all_rejected_leaves()

    # Create a dictionary containing the leave list
    dataset = {'leave_list_rejected': leave}

    # Render the leave list view
    return render(request, 'admin/leaves_rejected.html', dataset)


# function to view the details of a leave request of a paritcualar employee


def leaves_view(request, id):
    # check if user is authenticated and is a superuser, redirect to home page if not
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # get the leave object with the given id or return a 404 error if not found
    leave = get_object_or_404(Leave, id=id)

    # get the employee object associated with the user who made the leave request
    employee = Employee.objects.filter(user=leave.user)[0]

    # create a context dictionary containing the leave and employee objects, and a title string
    context = {'leave': leave,
               'employee': employee,
               'title': '{0}-{1} leave'.format(leave.user.username, leave.status)
               }

    # render the leave_detail.html template with the context dictionary and return the resulting HTML
    return render(request, 'admin/leave_detail.html', context)


# function used to approve a leave request


def approve_leave(request, id):
    # Check if the user is authenticated and is a superuser, if not redirect to home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get the leave object with the given id or return a 404 error page
    leave = get_object_or_404(Leave, id=id)

    # Approve the leave and save changes to the database
    leave.approve_leave()

    # Send an email notification to the user who requested the leave
    email = leave.user.username
    send_mail(
        'Leave Request Approved',
        'Dear {0},\n\nCongratulations! Your leave request has been approved!\n\nRegards,\nAdministration.'.format(
            leave.get_full_name),
        'hr.system.x@gmail.com',
        [email],
        fail_silently=False,
    )

    # Redirect to the detail view of the approved leave and display a success message
    messages.success(request, 'Leave successfully approved for {0}'.format(
        leave.get_full_name), extra_tags='alert alert-success alert-dismissible show')

    return redirect('admin_app:leave-employee', id=id)


# function used to unapprove a leave request


def unapprove_leave(request, id):
    # Check if user is authenticated and a superuser, otherwise redirect to home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get the leave instance by id
    leave = get_object_or_404(Leave, id=id)

    # Mark the leave as unapproved
    leave.unapprove_leave

    # Redirect to the leave list page
    return redirect('admin_app:leaves')


# function used to cancel a leave request.


def cancel_leave(request, id):
    # Check if the user is authenticated and a superuser
    if not (request.user.is_authenticated and request.user.is_superuser):
        # Redirect to the home page if the user is not authenticated or not a superuser
        return redirect('hris:home')

    # Get the leave object with the provided id or raise a 404 error if not found
    leave = get_object_or_404(Leave, id=id)

    # Cancel the leave
    leave.leaves_cancel

    # Add a success message to the request
    messages.success(request, 'Leave is canceled',
                     extra_tags='alert alert-success alert-dismissible show')

    # Redirect to the cancelled leaves page
    return redirect('admin_app:leaves-cancelled')


# This function is used to uncancel a cancelled leave request by changing its status to "pending"
def uncancel_leave(request, id):
    # check if user is authenticated and is a superuser, otherwise redirect to home page
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # get the leave object with the given id, otherwise raise a 404 error
    leave = get_object_or_404(Leave, id=id)

    # change the leave status to 'pending', set is_approved to False, and save the changes
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()

    # display success message to the user
    messages.success(request, 'Leave is uncanceled,now in pending list',
                     extra_tags='alert alert-success alert-dismissible show')

    # redirect the user to the cancelled leaves list
    return redirect('admin_app:leaves-cancelled')


# This function is to reject a leave request by an employee.

def reject_leave(request, id):

    # Check if the user is authenticated and a superuser
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    # Get the leave object from the provided id or throw 404 error
    leave = get_object_or_404(Leave, id=id)

    # Update leave status to rejected
    leave.reject_leave

    # Get the email address of the user whose leave is rejected
    email = leave.user.username

    # Send email notification to the user whose leave is rejected
    send_mail(
        'Leave Request Rejected',
        'Dear {0},\n\nWe regret to inform you that your leave request has been rejected.\n\nRegards,\nAdministration.'.format(
            leave.get_full_name),
        'hr.system.x@gmail.com',
        [email],
        fail_silently=False,
    )

    # Redirect to the rejected leaves page
    messages.success(request, 'Leave is rejected',
                     extra_tags='alert alert-success alert-dismissible show')
    return redirect('admin_app:leaves-rejected')


# Define the view function for unrejecting a leave.

def unreject_leave(request, id):
    # Check if the user is authenticated and a superuser, if not, redirect to home
    if not (request.user.is_authenticated and request.user.is_superuser):

        return redirect('hris:home')

    # Get the Leave object with the given id, or raise a 404 error if not found
    leave = get_object_or_404(Leave, id=id)

    # Set the status of the Leave object to 'pending' and is_approved to False and save the leave
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()

    # Show a success message
    messages.success(request, 'Leave is now in pending list ',
                     extra_tags='alert alert-success alert-dismissible show')

    # Redirect to the 'leaves-rejected' page
    return redirect('admin_app:leaves-rejected')
'''
