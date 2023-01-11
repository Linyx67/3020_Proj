from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    LeaveReport,
    Notification,
    Religion,
    Emergency,
    Employee,
    Leave
)


# Register your models here.
admin.site.register(Employee)
admin.site.register(LeaveReport)
admin.site.register(Notification)
admin.site.register(Religion)
admin.site.register(Emergency)
admin.site.register(Leave)
