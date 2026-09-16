from django.contrib import admin

from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "submitted_by", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "email", "location", "message")
