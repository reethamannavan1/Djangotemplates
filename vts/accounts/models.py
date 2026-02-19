from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('trainee', 'Trainee'),
        ('consultant', 'Consultant'),
    )

    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='trainee'
    )

    def __str__(self):
        return self.username




#whychooseus
class WhyChooseSection(models.Model):
    image = models.ImageField(upload_to="why_section/")
    circle_text = models.CharField(max_length=50, default="Why choose Us")

    def __str__(self):
        return "Why Choose Section"




class WhyChooseUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to="whychoose_icons/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Why Choose Us Item"
        verbose_name_plural = "Why Choose Us Items"

    def __str__(self):
        return self.title



#howvts works

class HowVTSWorksSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255)
    side_image = models.ImageField(upload_to="howvts/")

    def __str__(self):
        return self.title


class HowVTSWorksStep(models.Model):
    icon = models.ImageField(upload_to="howvts/icons/")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title




#studentsuccess
from django.db import models


class StudentProject(models.Model):
    title = models.CharField(max_length=200)
    student_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to="student_projects/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title



#testimonials
class StudentStory(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="student_stories/")
    
    youtube_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to="student_videos/", blank=True, null=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


#CTA
class CTASection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    button_text = models.CharField(max_length=100)
    button_link = models.CharField(max_length=200)
    image = models.ImageField(upload_to="cta/")

    def __str__(self):
        return self.title
