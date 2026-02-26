# jobs/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_alert, name="job_alert"),
]