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
        publications = Publications.objects.filter(
            user_id=id)
        jorunals = publications.filter(publicationtype='Peer Reviewed Journal')
        papers = publications.filter(publicationtype='Conference Paper')
        books = publications.filter(publicationtype='Book')
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
