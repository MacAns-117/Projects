from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_name", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("task_name", "description", "owner__username")
