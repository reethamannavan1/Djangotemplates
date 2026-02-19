from django.db import models

class AboutIntro(models.Model):
    main_title = models.CharField(max_length=200)
    subtitle = models.TextField()

    story_title = models.CharField(max_length=200)
    story_content = models.TextField()

    story_image = models.ImageField(upload_to='about/')

    def __str__(self):
        return self.main_title




from django.db import models

class AboutValue(models.Model):
    TYPE_CHOICES = (
        ('mission', 'Mission'),
        ('vision', 'Vision'),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    icon = models.ImageField(upload_to='about/icons/')
    title = models.CharField(max_length=100)
    description = models.TextField()

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
