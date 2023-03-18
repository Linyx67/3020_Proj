from django.shortcuts import (
    render,
    HttpResponse,
    redirect,
    HttpResponseRedirect,
    get_object_or_404
)
from django.contrib.auth import (
    logout,
    authenticate,
    login
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q, F

from django.http import FileResponse
import io
import re
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from staff_app.models import (
    Employee,
    Leave,
    Awards,
    Publications,
    Conferences,
    Development,
    Manuscripts,
    Presentations,
    Consultancies,
    Grants
)
from hris_app.models import CustomUser
# Create your views here.


def home(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    return render(request, "admin/admin_home.html")


def employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    dataset = dict()
    employees = Employee.objects.all().order_by('firstname')

    # pagination
    query = request.GET.get('search')
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        employees = employees.filter(
            Q(email__icontains=query)
        )

    paginator = Paginator(employees, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)

    dataset['employee_list'] = employees_paginated
    dataset['all_employees'] = Employee.objects.all_employees()

    blocked_employees = Employee.objects.all_blocked_employees()

    dataset['blocked_employees'] = blocked_employees
    dataset['title'] = 'Employees list view'

    return render(request, 'admin/view_employees.html', dataset)


def employees_info(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    if Employee.objects.filter(user_id=id).exists():
        employee = Employee.objects.get(user_id=id)
    else:
        employee = Employee.objects.none()

    if Awards.objects.filter(user_id=id).exists():
        awards = Awards.objects.filter(user_id=id)
    else:
        awards = Awards.objects.none()

    if Publications.objects.filter(user_id=id).exists():
        publications = Publications.objects.filter(user_id=id)
    else:
        publications = Publications.objects.none()

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
        manuscripts = Manuscripts.objects.filter(user_id=id)
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
    dataset['publications'] = publications
    dataset['grants'] = grants
    dataset['consultancies'] = consultancies
    dataset['presentations'] = presentations
    dataset['manuscripts'] = manuscripts
    dataset['development'] = development
    dataset['conferences'] = conferences
    dataset['title'] = 'profile - {0}'.format(employee.get_full_name)

    return render(request, "admin/employee_info.html", dataset)


def download_vitae(request, id):
    object = get_object_or_404(Employee, user_id=id)
    file = object.vitae.path
    response = FileResponse(open(file, 'rb'))
    return response


def leaves_list(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leaves = Leave.objects.all()
    context = {
        'leave_list': leaves,
        'title': 'ALL LEAVES'
    }
    return render(request, "admin/leaves_view.html", context)


def leaves_pending_list(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leaves = Leave.objects.all_pending_leaves()
    context = {
        'leave_list': leaves,
        'title': 'PENDING LEAVES'
    }
    return render(request, "admin/leaves_view.html", context)


def leaves_approved_list(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    leaves = Leave.objects.all_approved_leaves()

    context = {
        'leave_list': leaves,
        'title': 'approved leave list'
    }
    return render(request, 'admin/leaves_approved.html', context)


def cancel_leaves_list(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leaves = Leave.objects.all_cancelled_leaves()

    context = {
        'leave_list_cancel': leaves,
        'title': 'Cancel leave list'
    }

    return render(request, 'admin/leaves_cancelled.html', context)


def leave_rejected_list(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    dataset = dict()
    leave = Leave.objects.all_rejected_leaves()

    dataset['leave_list_rejected'] = leave
    return render(request, 'admin/leaves_rejected.html', dataset)


def leaves_view(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user)[0]
    context = {'leave': leave,
               'employee': employee,
               'title': '{0}-{1} leave'.format(leave.user.username, leave.status)
               }
    return render(request, 'admin/leave_detail.html', context)


def approve_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leave = get_object_or_404(Leave, id=id)
    leave.approve_leave
    email = leave.user.username
    messages.error(request, 'Leave successfully approved for {0}'.format(
        leave.get_full_name), extra_tags='alert alert-success alert-dismissible show')

    send_mail(
        'Leave Request Approved',
        'Dear {0},\n\nCongratulations! Your leave request has been approved!\n\nRegards,\nAdministration.'.format(
            leave.get_full_name),
        'hr.system.x@gmail.com',
        [email],
        fail_silently=False,
    )

    return redirect('admin_app:leave-employee', id=id)


def unapprove_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leave = get_object_or_404(Leave, id=id)
    leave.unapprove_leave
    return redirect('admin_app:leaves')  # redirect to unapproved list


def cancel_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leave = get_object_or_404(Leave, id=id)
    leave.leaves_cancel

    messages.success(request, 'Leave is canceled',
                     extra_tags='alert alert-success alert-dismissible show')
    # work on redirecting to instance leave - detail view
    return redirect('admin_app:leaves-cancelled')


# Current section -> here
def uncancel_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave is uncanceled,now in pending list',
                     extra_tags='alert alert-success alert-dismissible show')
    # work on redirecting to instance leave - detail view
    return redirect('admin_app:leaves-cancelled')


def reject_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    leave = get_object_or_404(Leave, id=id)
    leave.reject_leave
    email = leave.user.username
    messages.success(request, 'Leave is rejected',
                     extra_tags='alert alert-success alert-dismissible show')
    send_mail(
        'Leave Request Rejected',
        'Dear {0},\n\nWe regret to inform you that your leave request has been rejected.\n\nRegards,\nAdministration.'.format(
            leave.get_full_name),
        'hr.system.x@gmail.com',
        [email],
        fail_silently=False,
    )
    return redirect('admin_app:leaves-rejected')

    # return HttpResponse(id)


def unreject_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave is now in pending list ',
                     extra_tags='alert alert-success alert-dismissible show')

    return redirect('admin_app:leaves-rejected')


# Rabotec staffs leaves table user only
def view_my_leave_table(request):
    # work on the logics
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    else:
        user = request.user
        leaves = Leave.objects.filter(user=user)
        employee = Employee.objects.filter(user=user).first()
        print(leaves)
        dataset = dict()
        dataset['leave_list'] = leaves
        dataset['employee'] = employee
        dataset['title'] = 'Leaves List'
    return render(request, 'admin/staff_leaves_table.html', dataset)


def awards(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    awards = Awards.objects.prefetch_related('user').all().order_by('-year')
    dataset = dict()

    # pagination
    query = request.GET.get('search')
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        awards = awards.filter(
            Q(user__username__icontains=query)
        )

    paginator = Paginator(awards, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    awards_paginated = paginator.get_page(page)

    dataset['awards_list'] = awards_paginated
    dataset['all_awards'] = Awards.objects.all()

    dataset['title'] = 'Awards list view'

    return render(request, "admin/awards.html", dataset)


def publications(request):

    return render(request, "admin/publications_view.html")


def pubs_journals(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    publications = Publications.objects.prefetch_related('user').all().order_by(
        '-year')

    dataset = dict()
    # pagination
    query = request.GET.get('search')
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        publications = publications.filter(
            Q(user__username__icontains=query)
        )

    paginator = Paginator(publications, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    publications_paginated = paginator.get_page(page)

    dataset['pubs_list'] = publications_paginated
    dataset['all_pubs'] = Publications.objects.all()

    dataset['title'] = 'Publications list view'
    return render(request, "admin/publications_journals.html", dataset)
