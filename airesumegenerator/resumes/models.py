# resumes/models.py
from django.conf import settings
from django.db import models

class ResumeOptimization(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resume_optimizations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # your CustomUser has no username, use email
        return f"{self.user.email} - {self.created_at:%Y-%m-%d}"



#coverletter
class CoverLetter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} cover letter"




#createresume
from django.db import models
from django.conf import settings


class Resume(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes"
    )

    title = models.CharField(max_length=200)

    summary = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    




#templates
class Template(models.Model):
    TEMPLATE_TYPE = [
        ("resume", "Resume"),
        ("letter", "Letter"),
        ("website", "Website"),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="templates/")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=TEMPLATE_TYPE, default="resume")

    def __str__(self):
        return self.name
    



class UserTemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "template")

    def __str__(self):
        return f"{self.user} owns {self.template}"