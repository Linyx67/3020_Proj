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
from .models import (
    Employee,
    Requests,
    Awards,
    Publications,
    Conferences,
    Consultancies,
    Manuscripts,
    Development,
    Presentations,
    Grants,
    Specialisation,
    Supervision,
    Research,
    Roles,
    Honours,
    Contributions,
    Activities,
    Contacts
)
from .functions import get_user_info
from .forms import (
    AwardsCreateForm,
    PublicationsCreateForm,
    EmployeeCreateForm,
    RequestsCreateForm,
    ConferencesCreateForm,
    PresentationsCreateForm,
    DevelopmentCreateForm,
    ConsultanciesCreateForm,
    ManuscriptsCreateForm,
    GrantsCreateForm,
    RolesCreateForm,
    ResearchCreateForm,
    SupervisionCreateForm,
    SpecialisationCreateForm,
    HonoursCreateForm,
    ActivitiesCreateForm,
    ContributionsCreateForm
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
        messages.success(request, "Profile Updated")
        # Redirect to the profile view
        return redirect('staff:profile')

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
        messages.success(request, "Saved successfully")
        # Redirect to the awards view
        return redirect('staff:award')

    # Pass the form to the template for rendering
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)


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
        messages.success(request, "Saved successfully")
        return redirect('staff:award')

    # Pass the form to the template for rendering
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete award


def delete_award(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the award object with the specified id, or raise a 404 error if it doesn't exist
    awards = get_object_or_404(Awards, id=id)

    # Delete the award object
    awards.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the awards view
    return redirect('staff:award')


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
        messages.success(request, "Added successfully")
        # Redirect to the publications page
        return redirect('staff:publication')

    # If the form is not valid, render the staff_publications_edit
    # template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)


def edit_publication(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the publication object with the specified id
    publications = get_object_or_404(Publications, id=id)

    # Create a new instance of the PublicationsCreateForm,
    # passing in the publication object as an instance
    form = PublicationsCreateForm(request.POST or None, instance=publications)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the publications page
        return redirect('staff:publication')

    # If the form is not valid, render the staff_publications_edit
    # template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete publication


def publication_delete(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the publication object with the specified id
    publications = get_object_or_404(Publications, id=id)

    # Delete the publication object
    publications.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the publications page
    return redirect('staff:publication')


def view_publications(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not, redirect to the home page
        return redirect('hris:home')

    # Check if the logged-in user has any publications
    if Publications.objects.filter(user_id=request.user.id).exists():
        # If there are publications, retrieve them and
        # store them in the "publications" variable
        publications = Publications.objects.filter(user_id=request.user.id)
    else:
        # If there are no publications,
        # store an empty list in the "publications" variable
        publications = []

    # Pass the "publications" variable to the
    # "staff/staff_publications.html" template as "object"
    context = {
        "object": publications
    }
    return render(request, "staff/staff_publications.html", context)

# view requests


def rfi(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    rfis = Requests.objects.filter(user_id=request.user.id)

    context = {
        "object": rfis
    }
    return render(request, "staff/staff_rfi_view.html", context)
# add Request for Information


def rfi_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Request creation object based on the request's POST data
    form = RequestsCreateForm(request.POST or None)

    # If form is valid, save the request request and redirect to the staff view page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Request Submitted successfully")
        return redirect('staff:requests')

    # If form is not valid, render the staff_leave_add template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Request For Information


def rfi_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Get the request object with the specified id
    rfis = get_object_or_404(Requests, id=id)

    # Delete the request object
    rfis.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the requests page
    return redirect('staff:requests')

# view conference entries


def conferences_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    conferences = Conferences.objects.filter(user_id=request.user.id)

    context = {
        "object": conferences
    }
    return render(request, "staff/staff_conferences.html", context)

# add conference attended


def conferences_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Conference CreateForm object based on the request's POST data
    form = ConferencesCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:conference')

    # If form is not valid, render the staff_leave_add template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit conference entry


def conferences_edit(request, id):
    # Get the confernece object with the specified id
    conference = get_object_or_404(Conferences, id=id)

    # Create a new instance of the Conferences create form, passing in the confernece object as an instance
    form = ConferencesCreateForm(request.POST or None, instance=conference)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:conference')

    # If the form is not valid, render the add conference  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete conference entry


def conferences_delete(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the conference object with the specified id
    conference = get_object_or_404(Conferences, id=id)

    # Delete the conference object
    conference.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:conference')


# view technical presentation entries
def presentations_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    presentations = Presentations.objects.filter(user_id=request.user.id)

    context = {
        "object": presentations
    }
    return render(request, "staff/staff_presentations.html", context)
# add technical presentation


def presentations_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Presentations CreateForm object based on the request's POST data
    form = PresentationsCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:presentations')

    # If form is not valid, render the staff presentations template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit presentation entry


def presentations_edit(request, id):
    # Get the presentation object with the specified id
    presentation = get_object_or_404(Presentations, id=id)

    # Create a new instance of the Presentations create form, passing in the presentation object as an instance
    form = PresentationsCreateForm(request.POST or None, instance=presentation)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:presentations')

    # If the form is not valid, render the add presentation  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)


# delete presentations


def presentations_delete(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the presentation object with the specified id
    presentation = get_object_or_404(Presentations, id=id)

    # Delete the presentation object
    presentation.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:presentations')

# view professional development entries


def development_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    development = Development.objects.filter(user_id=request.user.id)

    context = {
        "object": development
    }
    return render(request, "staff/staff_development.html", context)

# add professional development entry


def development_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Professional Development CreateForm object based on the request's POST data
    form = DevelopmentCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:development')

    # If form is not valid, render the staff developent template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit professional development entry


def development_edit(request, id):
    # Get the development object with the specified id
    development = get_object_or_404(Development, id=id)

    # Create a new instance of the Professional Development create form, passing in the development object as an instance
    form = DevelopmentCreateForm(request.POST or None, instance=development)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:development')

    # If the form is not valid, render the add development  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete professional development entry


def development_delete(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the development object with the specified id
    development = get_object_or_404(Development, id=id)

    # Delete the development object
    development.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:development')

# view consultancies


def consultancies_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    consultancies = Consultancies.objects.filter(user_id=request.user.id)

    context = {
        "object": consultancies
    }
    return render(request, "staff/staff_consultancies.html", context)

# add Consultancy entry


def consultancies_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Consultancies CreateForm object based on the request's POST data
    form = ConsultanciesCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:consultancies')

    # If form is not valid, render the staff consultancies template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Consultancy entry


def consultancies_edit(request, id):
    # Get the consultancy object with the specified id
    consultancy = get_object_or_404(Consultancies, id=id)

    # Create a new instance of the Consultancies create form, passing in the consultancy object as an instance
    form = ConsultanciesCreateForm(request.POST or None, instance=consultancy)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:consultancies')

    # If the form is not valid, render the add consultancy  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Consultancy entry


def consultancies_delete(request, id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the home page
        return redirect('hris:home')

    # Get the consultancy object with the specified id
    consultancy = get_object_or_404(Consultancies, id=id)

    # Delete the consultancy object
    consultancy.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:consultancies')

# view manuscript entries


def manuscripts_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    manuscripts = Manuscripts.objects.filter(user_id=request.user.id)

    context = {
        "object": manuscripts
    }
    return render(request, "staff/staff_manuscripts.html", context)

# add Manuscripts entry


def manuscripts_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Manuscripts CreateForm object based on the request's POST data
    form = ManuscriptsCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:manuscripts')

    # If form is not valid, render the staff manuscripts template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Manuscripts entry


def manuscripts_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the manuscript object with the specified id
    manuscript = get_object_or_404(Manuscripts, id=id)

    # Create a new instance of the Manuscripts create form, passing in the manuscript object as an instance
    form = ManuscriptsCreateForm(request.POST or None, instance=manuscript)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:manuscripts')

    # If the form is not valid, render the add manuscript  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Manuscripts entry


def manuscripts_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the manuscript object with the specified id
    manuscript = get_object_or_404(Manuscripts, id=id)
    # Delete the manuscript object
    manuscript.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:manuscripts')

# view grants entries


def grants_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    grants = Grants.objects.filter(user_id=request.user.id)

    context = {
        "object": grants
    }
    return render(request, "staff/staff_grants.html", context)

# add grants entry


def grants_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Grants CreateForm object based on the request's POST data
    form = GrantsCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:grants')

    # If form is not valid, render the staff grants template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit grants entry


def grants_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the grant object with the specified id
    grant = get_object_or_404(Grants, id=id)

    # Create a new instance of the Grants create form, passing in the grant object as an instance
    form = GrantsCreateForm(request.POST or None, instance=grant)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:grants')

    # If the form is not valid, render the add grant  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete grants entry


def grants_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the grant object with the specified id
    grant = get_object_or_404(Grants, id=id)
    # Delete the grant object
    grant.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:grants')

# view Professional Role entries


def roles_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    roles = Roles.objects.filter(user_id=request.user.id)

    context = {
        "object": roles
    }
    return render(request, "staff/staff_roles.html", context)

# add Professional Role entry


def roles_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Roles CreateForm object based on the request's POST data
    form = RolesCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:roles')

    # If form is not valid, render the staff roles template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Professional Role entry


def roles_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the role object with the specified id
    role = get_object_or_404(Roles, id=id)

    # Create a new instance of the Roles create form, passing in the role object as an instance
    form = RolesCreateForm(request.POST or None, instance=role)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:roles')

    # If the form is not valid, render the add role  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Professional Role entry


def roles_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the role object with the specified id
    role = get_object_or_404(Roles, id=id)
    # Delete the role object
    role.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:roles')

# view Research Interest entries


def research_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    research = Research.objects.filter(user_id=request.user.id)

    context = {
        "object": research
    }
    return render(request, "staff/staff_research.html", context)


# add Research Interest entry
def research_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Research CreateForm object based on the request's POST data
    form = ResearchCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:research')

    # If form is not valid, render the staff research template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Research Interest entry


def research_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the research object with the specified id
    research = get_object_or_404(Research, id=id)

    # Create a new instance of the Research create form, passing in the research object as an instance
    form = ResearchCreateForm(request.POST or None, instance=research)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:research')

    # If the form is not valid, render the add research  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Research Interest entry


def research_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the research object with the specified id
    research = get_object_or_404(Research, id=id)
    # Delete the research object
    research.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:research')

# view Supervision entries


def supervision_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    supervision = Supervision.objects.filter(user_id=request.user.id)

    context = {
        "object": supervision
    }
    return render(request, "staff/staff_supervision.html", context)

# add Supervision entry


def supervision_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Supervision CreateForm object based on the request's POST data
    form = SupervisionCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:supervision')

    # If form is not valid, render the staff supervision template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Supervision entry


def supervision_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the supervision object with the specified id
    supervision = get_object_or_404(Supervision, id=id)

    # Create a new instance of the Supervision create form, passing in the supervision object as an instance
    form = SupervisionCreateForm(request.POST or None, instance=supervision)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:supervision')

    # If the form is not valid, render the add supervision  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Supervision entry


def supervision_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the supervision object with the specified id
    supervision = get_object_or_404(Supervision, id=id)
    # Delete the supervision object
    supervision.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:supervision')

# view Specialisation entries


def specialisation_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    specialisation = Specialisation.objects.filter(user_id=request.user.id)

    context = {
        "object": specialisation
    }
    return render(request, "staff/staff_specialisation.html", context)

# add Specialisation entry


def specialisation_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Specialisation CreateForm object based on the request's POST data
    form = SpecialisationCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:specialisation')

    # If form is not valid, render the staff specialisation template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Specialisation entry


def specialisation_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the specialisation object with the specified id
    specialisation = get_object_or_404(Specialisation, id=id)

    # Create a new instance of the Specialisation create form, passing in the specialisation object as an instance
    form = SpecialisationCreateForm(
        request.POST or None, instance=specialisation)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:specialisation')

    # If the form is not valid, render the add specialisation  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Specialisation entry


def specialisation_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the specialisation object with the specified id
    specialisation = get_object_or_404(Specialisation, id=id)
    # Delete the specialisation object
    specialisation.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:specialisation')

# view Professional Activity entries


def activity_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    activity = Activities.objects.filter(user_id=request.user.id)

    context = {
        "object": activity
    }
    return render(request, "staff/staff_activity.html", context)

# add Professional Activity


def activity_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Professional Activity CreateForm object based on the request's POST data
    form = ActivitiesCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:activity')

    # If form is not valid, render the staff professional activity template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Professional Activity


def activity_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the professional activity object with the specified id
    activity = get_object_or_404(Activities, id=id)

    # Create a new instance of the Professional Activity create form, passing in the professional activity object as an instance
    form = ActivitiesCreateForm(request.POST or None, instance=activity)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:activity')

    # If the form is not valid, render the add professional activity  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Professional Activity


def activity_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the professional activity object with the specified id
    activity = get_object_or_404(Activities, id=id)
    # Delete the professional activity object
    activity.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:activity')

# view honours or certificates entries


def honour_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    honours = Honours.objects.filter(user_id=request.user.id)

    context = {
        "object": honours
    }
    return render(request, "staff/staff_honours.html", context)

# add Honours or Certificates


def honour_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Honours or Certificates CreateForm object based on the request's POST data
    form = HonoursCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:honours')

    # If form is not valid, render the staff honours or certificates template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Honours or Certificates


def honour_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the honours or certificates object with the specified id
    honour = get_object_or_404(Honours, id=id)

    # Create a new instance of the Honours or Certificates create form, passing in the honours or certificates object as an instance
    form = HonoursCreateForm(request.POST or None, instance=honour)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:honours')

    # If the form is not valid, render the add honours or certificates  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Honours or Certificates


def honour_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the honours or certificates object with the specified id
    honour = get_object_or_404(Honours, id=id)
    # Delete the honours or certificates object
    honour.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:honours')

# view Contributions to the department, faculty, university entries


def contribution_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    contributions = Contributions.objects.filter(user_id=request.user.id)

    context = {
        "object": contributions
    }
    return render(request, "staff/staff_contributions.html", context)

# add Contributions to the department, faculty, university


def contribution_add(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    # Create a Contributions to the department, faculty, university CreateForm object based on the request's POST data
    form = ContributionsCreateForm(request.POST or None)

    # If form is valid, save the form and redirect to the staff profile page
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Added successfully")
        return redirect('staff:contributions')

    # If form is not valid, render the staff contributions to the department, faculty, university template with the form as context
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# edit Contributions to the department, faculty, university


def contribution_edit(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the contributions to the department, faculty, university object with the specified id
    contribution = get_object_or_404(Contributions, id=id)

    # Create a new instance of the Contributions to the department, faculty, university create form, passing in the contributions to the department, faculty, university object as an instance
    form = ContributionsCreateForm(request.POST or None, instance=contribution)

    # Check if the form is valid
    if form.is_valid():
        # Save the form data to the database
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        messages.success(request, "Saved successfully")
        # Redirect to the profile page
        return redirect('staff:contributions')

    # If the form is not valid, render the add contributions to the department, faculty, university  template with the form object
    context = {
        'form': form
    }
    return render(request, "staff/staff_edit.html", context)

# delete Contributions to the department, faculty, university


def contribution_delete(request, id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')
    # Get the contributions to the department, faculty, university object with the specified id
    contribution = get_object_or_404(Contributions, id=id)
    # Delete the contributions to the department, faculty, university object
    contribution.delete()
    messages.success(request, "Deleted successfully")
    # Redirect to the profile page
    return redirect('staff:contributions')
# view contacts list


def contacts_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('hris:home')

    contacts = Contacts.objects.all()

    context = {
        "object": contacts
    }
    return render(request, "staff/staff_contacts.html", context)


'''
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
        messages.success(request, "Leave request submitted successfully")
        return redirect('staff:staff-home')

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
    '''
