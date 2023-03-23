from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Emergency,
    Employee,
    Leave,
    Awards,
    Publications,
    Conferences,
    Development,
    Manuscripts,
    Presentations,
    Consultancies,
    Grants,
    Roles,
    Research,
    Specialisation,
    Supervision

)


# Register your models here.
admin.site.register(Employee)
admin.site.register(Emergency)
admin.site.register(Leave)
admin.site.register(Awards)
admin.site.register(Publications)
admin.site.register(Consultancies)
admin.site.register(Conferences)
admin.site.register(Development)
admin.site.register(Manuscripts)
admin.site.register(Presentations)
admin.site.register(Grants)
admin.site.register(Roles)
admin.site.register(Research)
admin.site.register(Supervision)
admin.site.register(Specialisation)
