import datetime
from .models import (
    Employee,
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
    Activities,
    Contributions,
    Honours
)
from hris_app.models import CustomUser

# These are helper functions that return year choices for forms.

# creates a list of tuples of choices from 1900 to current year


def year_choices():
    return [(r, r) for r in range(datetime.date.today().year+1, 1900, -1)]

# creates a list of choices from 1900 to current year


def year_choice():
    return [r for r in range(datetime.date.today().year+1, 1900, -1)]

# creates a list of choices for academic year from 1980/1981 to current academic year


def academic_year_choices():
    return [((str(r)+'/'+str(r+1)), (str(r)+'/'+str(r+1))) for r in range(datetime.date.today().year, 1980, -1)]


# function to retrieve all relevant user info for displaying on
# a user's profile page
def get_user_info(id):

    # Check if Employee with given user ID exists
    if Employee.objects.filter(user_id=id).exists():
        # If it exists, retrieve the Employee object
        employee = Employee.objects.get(user_id=id)
    else:
        # If it doesn't exist, return an empty QuerySet
        employee = Employee.objects.none()

    # Retrieve all Awards objects for the given user ID
    awards = Awards.objects.filter(user_id=id)

    # Retrieve all Publications objects that are
    publications = Publications.objects.filter(user_id=id)
    # journals for the given user ID
    journals = Publications.objects.journals().filter(user_id=id)

    # Retrieve all Publications objects
    # that are papers for the given user ID
    papers = Publications.objects.papers().filter(user_id=id)

    # Retrieve all Publications
    # objects that are books for the given user ID
    books = Publications.objects.books().filter(user_id=id)

    # Retrieve all Grants objects for the given user ID
    grants = Grants.objects.filter(user_id=id)

    # Retrieve all Consultancies objects for the given user ID
    consultancies = Consultancies.objects.filter(user_id=id)

    # Retrieve all Presentations objects for the given user ID
    presentations = Presentations.objects.filter(user_id=id)

    # Retrieve all Manuscripts objects for the given user ID,
    # ordered by the 'status' field
    manuscripts = Manuscripts.objects.filter(
        user_id=id).order_by('status')

    # Retrieve all Development objects for the given user ID
    development = Development.objects.filter(user_id=id)

    # Retrieve all Conferences objects for the given user ID
    conferences = Conferences.objects.filter(user_id=id)

    # Retrieve all Specialisation objects for the given user ID
    specialisation = Specialisation.objects.filter(user_id=id)

    # Retrieve all Supervision objects for the given user ID
    supervision = Supervision.objects.filter(user_id=id)

    # Retrieve all Research objects for the given user ID
    research = Research.objects.filter(user_id=id)

    # Retrieve all Roles objects for the given user ID
    roles = Roles.objects.filter(user_id=id)

    # Retrieve all Activities objects for the given user ID
    activities = Activities.objects.filter(user_id=id)

    # Retrieve all Contributions objects for the given user ID
    contributions = Contributions.objects.filter(user_id=id)

    # retrieve all Honours objects for the given user ID
    honours = Honours.objects.filter(user_id=id)

    # Create a dictionary containing all the retrieved data
    dataset = {
        'employee': employee,
        'awards': awards,
        'publications': publications,
        'journals': journals,
        'papers': papers,
        'books': books,
        'grants': grants,
        'consultancies': consultancies,
        'presentations': presentations,
        'manuscripts': manuscripts,
        'development': development,
        'conferences': conferences,
        'specialisation': specialisation,
        'supervision': supervision,
        'research': research,
        'roles': roles,
        'honours': honours,
        'activities': activities,
        'contributions': contributions,
    }

    # Return the dictionary
    return dataset
