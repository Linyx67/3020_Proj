
from django.core.mail import send_mail
from staff_app.models import (
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


def rfi_api():
    '''
    this function first gets all the ids of the active employyees then it checks to see if there are entries
    in every database table relating to these employee ids. If there are no entries then it sends an email
    to the employee urging them to update these tables.
    '''
    ids = Employee.objects.all().values_list('user_id', flat=True)
    for id in ids:
        employee = Employee.objects.get(user_id=id)
        if not Development.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Professional Development Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )

        if not Awards.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Received Awards Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Publications.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Publication Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Conferences.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Attended Conferences Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Roles.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your University Professional Service Roles Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Research.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Research Interests Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Specialisation.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Academic Specialisation Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Supervision.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Postgraduate Supervision Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Consultancies.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Professional Consultancies Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Grants.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Research Grants Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Presentations.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Technical Presentations Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
        if not Manuscripts.objects.filter(user_id=id).exists():
            send_mail(
                'Request For Infomation',
                'Dear {0},\n\nIt seems as though you have not entered your Manuscripts Information as yet. If you do not know where to find this it is under the profile section of the site. Please update this information as soon as possible.\n\nRegards,\nAdministration.'.format(
                    employee.get_full_name),
                'hr.system.x@gmail.com',
                [employee.email],
                fail_silently=False,
            )
