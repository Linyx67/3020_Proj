from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
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

from hris_app .models import CustomUser
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
from staff_app.functions import get_user_info
from .filters import EmployeeFilter
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
    dataset = get_user_info(id)
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
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    publications = Publications.objects.prefetch_related('user').all().order_by(
        '-year')

    dataset = dict()

    query = request.GET.get('search')
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        publications = publications.filter(
            Q(user__username__icontains=query)
        )

    # pagination
    paginator = Paginator(publications, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    publications_paginated = paginator.get_page(page)

    dataset['pubs_list'] = publications_paginated
    dataset['all_pubs'] = Publications.objects.all()

    dataset['title'] = 'Employee | Publications'
    dataset['count_title'] = 'Total Publications'

    return render(request, "admin/publications_view.html", dataset)


def pubs_journals(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    journals = Publications.objects.journals().prefetch_related('user').all().order_by(
        '-year')

    dataset = dict()
    dataset['all_pubs'] = journals

    query = request.GET.get('search')
    # fix the query as the count gets reset when a query happens
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        journals = journals.filter(
            Q(user__username__icontains=query)
        )

    # pagination
    paginator = Paginator(journals, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    journals_paginated = paginator.get_page(page)

    dataset['pubs_list'] = journals_paginated

    dataset['title'] = 'Publications | Journals'
    dataset['count_title'] = 'Total Journals'

    return render(request, "admin/publications_view.html", dataset)


def pubs_papers(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    papers = Publications.objects.papers().prefetch_related('user').all().order_by(
        '-year')

    dataset = dict()
    dataset['all_pubs'] = papers

    query = request.GET.get('search')
    # fix the query as the count gets reset when a query happens
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        papers = papers.filter(
            Q(user__username__icontains=query)
        )

    # pagination
    paginator = Paginator(papers, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    papers_paginated = paginator.get_page(page)

    dataset['pubs_list'] = papers_paginated

    dataset['title'] = 'Publications | Conference Papers'
    dataset['count_title'] = 'Total Papers'

    return render(request, "admin/publications_view.html", dataset)


def pubs_books(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    books = Publications.objects.books().prefetch_related('user').all().order_by(
        '-year')

    dataset = dict()
    dataset['all_pubs'] = books

    query = request.GET.get('search')
    # fix the query as the count gets reset when a query happens
    if query:
        query = re.sub(r"\s+", ".", query, flags=re.UNICODE)
        books = books.filter(
            Q(user__username__icontains=query)
        )

    # pagination
    paginator = Paginator(books, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    books_paginated = paginator.get_page(page)

    dataset['pubs_list'] = books_paginated

    dataset['title'] = 'Publications | Books'
    dataset['count_title'] = 'Total Books'

    return render(request, "admin/publications_view.html", dataset)


def annualreports(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')

    dataset = dict()
    users = CustomUser.objects.none()
    publications = Publications.objects.none()
    presentations = Presentations.objects.none()
    conferences = Conferences.objects.none()
    awards = Awards.objects.none()
    # myFilter = EmployeeFilter(request.GET, queryset=employees)
    # employees = myFilter.qs
    if request.GET.get('first_name'):
        firstname = request.GET.get('first_name')
        lastname = request.GET.get('last_name')
        year = request.GET.get('year')
        if CustomUser.objects.filter(first_name=firstname, last_name=lastname).exists():
            users = CustomUser.objects.get(
                first_name=firstname, last_name=lastname)
            publications = Publications.objects.filter(
                user_id=users.id, year=year)
            presentations = Presentations.objects.filter(
                user_id=users.id, year=year)
            conferences = Conferences.objects.filter(
                user_id=users.id, year=year)
            awards = Awards.objects.filter(user_id=users.id, year=year)

    dataset['users'] = users
    dataset['awards'] = awards
    dataset['publications'] = publications
    dataset['presentations'] = presentations
    dataset['conferences'] = conferences

    return render(request, 'admin/annualreports.html', dataset)
