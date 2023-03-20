from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Religion,
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
    Grants
)


# Register your models here.
admin.site.register(Employee)
admin.site.register(Religion)
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
