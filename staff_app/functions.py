import datetime
from .models import (
    Employee,
    Awards,
    Publications,
    Conferences,
    Development,
    Manuscripts,
    Presentations,
    Consultancies,
    Grants
)


def year_choices():
    return [(r, r) for r in range(datetime.date.today().year+1, 1900, -1)]


def year_choice():
    return [r for r in range(datetime.date.today().year+1, 1900, -1)]


def academic_year_choices():
    return [((str(r)+'/'+str(r+1)), (str(r)+'/'+str(r+1))) for r in range(datetime.date.today().year, 1950, -1)]


def get_user_info(id):

    if Employee.objects.filter(user_id=id).exists():
        employee = Employee.objects.get(user_id=id)
    else:
        employee = Employee.objects.none()

    if Awards.objects.filter(user_id=id).exists():
        awards = Awards.objects.filter(user_id=id)
    else:
        awards = Awards.objects.none()

    if Publications.objects.filter(user_id=id).exists():
        jorunals = Publications.objects.journals().filter(user_id=id)
        papers = Publications.objects.papers().filter(user_id=id)
        books = Publications.objects.books().filter(user_id=id)
    else:
        publications = Publications.objects.none()
        jorunals = publications.none()
        papers = publications.none()
        books = publications.none()

    if Grants.objects.filter(user_id=id).exists():
        grants = Grants.objects.filter(user_id=id)
    else:
        grants = Grants.objects.none()

    if Consultancies.objects.filter(user_id=id).exists():
        consultancies = Consultancies.objects.filter(user_id=id)
    else:
        consultancies = Consultancies.objects.none()

    if Presentations.objects.filter(user_id=id).exists():
        presentations = Presentations.objects.filter(user_id=id)
    else:
        presentations = Presentations.objects.none()

    if Manuscripts.objects.filter(user_id=id).exists():
        manuscripts = Manuscripts.objects.filter(
            user_id=id).order_by('in_preparation')
    else:
        manuscripts = Manuscripts.objects.none()

    if Development.objects.filter(user_id=id).exists():
        development = Development.objects.filter(user_id=id)
    else:
        development = Development.objects.none()

    if Conferences.objects.filter(user_id=id).exists():
        conferences = Conferences.objects.filter(user_id=id)
    else:
        conferences = Conferences.objects.none()

    dataset = dict()
    dataset['employee'] = employee

    dataset['awards'] = awards
    dataset['journals'] = jorunals
    dataset['papers'] = papers
    dataset['books'] = books
    dataset['grants'] = grants
    dataset['consultancies'] = consultancies
    dataset['presentations'] = presentations
    dataset['manuscripts'] = manuscripts
    dataset['development'] = development
    dataset['conferences'] = conferences
    dataset['title'] = 'profile - {0}'.format(employee.get_full_name)

    return dataset
