from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from hris_app.models import StaffUser, CustomUser
from .models import LeaveReport, Notification
# Create your views here.


def home(request):
    print(request.user.id)
    # Fetch All Approve Leave
    # print(request.user)
    print(request.user.user_type)
    staff = StaffUser.objects.get(admin=request.user.id)
    leave_count = LeaveReport.objects.filter(
        staff_id=staff.id, leave_status=1).count()
    context = {
        "leave_count": leave_count,
    }

    return render(request, 'staff_home.html', context)


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
    user = CustomUser.objects.get(id=request.user.id)
    staff = StaffUser.objects.get(admin=user)

    context = {
        "user": user,
        "staff": staff
    }
    return render(request, "staff_profile.html", context)


def profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = StaffUser.objects.get(admin=customuser.id)
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('profile')

        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('profile')
