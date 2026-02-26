# jobs/admin.py


from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("company", "title", "location", "job_type", "posted_days")
    search_fields = ("company", "title", "location")
    list_filter = ("job_type", "location")