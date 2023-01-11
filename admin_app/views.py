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
from staff_app.models import Employee
# Create your views here.


def employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    employees = Employee.objects.all()

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

    return render(request, 'dashboard/employee_app.html', dataset)
