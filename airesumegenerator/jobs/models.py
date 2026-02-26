# jobs/models.py

from django.db import models

class Job(models.Model):
    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, default="Full Time")
    posted_days = models.IntegerField(default=1)   # UI shows 18d etc

    def __str__(self):
        return f"{self.company} - {self.title}"