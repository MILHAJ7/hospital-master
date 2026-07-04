from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Prescription

from .models import (
    CustomUser,
    Doctor,
    Patient,
    Appointment
)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)