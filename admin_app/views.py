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
from django.contrib import messages
from django.db.models import Q
from staff_app.models import Employee, Leave, Awards, Publications
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
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
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

    employee = get_object_or_404(Employee, id=id)

    dataset = dict()
    dataset['employee'] = employee
    dataset['title'] = 'profile - {0}'.format(employee.get_full_name)

    return render(request, "admin/employee_info.html", dataset)


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
    # approved leaves -> calling model manager method
    leaves = Leave.objects.all_approved_leaves()

    context = {
        'leave_list': leaves,
        'title': 'approved leave list'
    }
    return render(request, 'admin/leaves_approved.html', context)


def cancel_leaves_list(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    leaves = Leave.objects.all_cancel_leaves()

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
    user = leave.user
    employee = Employee.objects.filter(user=user)[0]
    leave.approve_leave

    messages.error(request, 'Leave successfully approved for {0}'.format(
        employee.get_full_name), extra_tags='alert alert-success alert-dismissible show')
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
    dataset = dict()
    leave = get_object_or_404(Leave, id=id)
    leave.reject_leave
    messages.success(request, 'Leave is rejected',
                     extra_tags='alert alert-success alert-dismissible show')
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
    awards = Awards.objects.all().order_by('-year')

    context = {
        "awards": awards,
    }
    return render(request, "admin/awards.html", context)


def publications(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('hris:home')
    publications = Publications.objects.all().order_by('-year')

    context = {
        "publications": publications,
    }
    return render(request, "admin/publications.html", context)
