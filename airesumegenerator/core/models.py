from django.db import models


class HeroSection(models.Model):
    badge_text = models.CharField(max_length=100)
    heading = models.CharField(max_length=300)
    subtext = models.TextField()

    primary_button = models.CharField(max_length=50)
    secondary_button = models.CharField(max_length=50)

    hero_image = models.ImageField(upload_to="hero/")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Homepage Hero"