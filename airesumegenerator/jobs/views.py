# jobs/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job


@login_required
def job_alert(request):

    jobs = Job.objects.all().order_by("-id")

    # ⭐ SEARCH FILTER
    keyword = request.GET.get("keyword")
    location = request.GET.get("location")

    if keyword:
        jobs = jobs.filter(title__icontains=keyword) | jobs.filter(company__icontains=keyword)

    if location:
        jobs = jobs.filter(location__icontains=location)

    # ⭐ MASTER DETAIL
    selected_job = None
    job_id = request.GET.get("job")

    if job_id:
        selected_job = get_object_or_404(Job, id=job_id)
    elif jobs:
        selected_job = jobs.first()

    return render(request, "dashboard/job_alert.html", {
        "jobs": jobs,
        "selected_job": selected_job
    })