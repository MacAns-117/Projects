from django.contrib import admin

from .models import Nurse, Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "age", "disease", "location")
    search_fields = ("name", "disease", "location")


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "shift", "experience", "email")
    list_filter = ("department", "shift")
    search_fields = ("name", "email")
