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
from .models import LeaveReport, Notification, Employee, Publications, Awards
from .forms import AwardsCreateForm, PublicationsCreateForm, EmployeeCreateForm
# Create your views here.


def home(request):
    return render(request, 'staff_home.html')


def apply_leave(request):
    print(request.user.id)
    staff_obj = StaffUser.objects.get(admin=request.user.id)
    leave_data = LeaveReport.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return (request, "staff_apply_leave.html", context)


def apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        staff_obj = StaffUser.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReport(
                staff_id=staff_obj,
                leave_date=leave_date,
                leave_message=leave_message,
                leave_status=0
            )
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('apply_leave')


def profile(request):
    employee = get_object_or_404(Employee, user_id=request.user.id)
    # queryset = Employee.objects.filter(id=7)

    context = {
        "object": employee
    }
    return render(request, "staff_profile.html", context)

# old code
# def profile_update(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('profile')
#     else:
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         password = request.POST.get('password')

#         try:
#             customuser = CustomUser.objects.get(id=request.user.id)
#             customuser.first_name = first_name
#             customuser.last_name = last_name
#             if password != None and password != "":
#                 customuser.set_password(password)
#             customuser.save()

#             staff = StaffUser.objects.get(admin=customuser.id)
#             staff.save()

#             messages.success(request, "Profile Updated Successfully")
#             return redirect('profile')

#         except:
#             messages.error(request, "Failed to Update Profile")
#             return redirect('profile')


def profile_update(request):

    employee = get_object_or_404(Employee, user_id=request.user.id)
    form = EmployeeCreateForm(request.POST or None, instance=employee)
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        return redirect('/staff_view')

    context = {
        'form': form
    }
    return render(request, "staff_profile_edit.html", context)


def add_award(request):
    form = AwardsCreateForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        return redirect('/staff_view/awards')
    context = {
        'form': form
    }
    return render(request, "staff_awards_add.html", context)


def edit_award(request):
    awards = get_object_or_404(Awards, user_id=request.user.id)
    form = AwardsCreateForm(request.POST or None, instance=awards)
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        return redirect('/staff_view/awards')
    context = {
        'form': form
    }
    return render(request, "staff_awards_edit.html", context)


def view_awards(request):
    awards = get_object_or_404(Awards, user_id=request.user.id)
    context = {
        "object": awards
    }
    return render(request, 'staff_awards.html', context)


def add_publication(request):
    form = PublicationsCreateForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        return redirect('/staff_view/publications')

    context = {
        'form': form
    }
    return render(request, "staff_publications_edit.html", context)


def edit_publication(request):
    publications = get_object_or_404(Publications, user_id=request.user.id)
    form = PublicationsCreateForm(request.POST or None, instance=publications)
    if form.is_valid():
        instance = form.save(commit='false')
        instance.user = request.user
        instance.save()
        return redirect('/staff_view/publications')

    context = {
        'form': form
    }
    return render(request, "staff_publications_edit.html", context)


def view_publications(request):
    publications = get_object_or_404(Publications, user_id=request.user.id)
    print(publications)
    context = {
        "object": publications
    }
    return render(request, 'staff_publications.html', context)
