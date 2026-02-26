from django.db import models
from django.conf import settings

class ToolUsage(models.Model):
    TOOL_TYPE = [
        ("pdf", "PDF"),
        ("image", "Image"),
        ("screenshot", "Screenshot"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tool = models.CharField(max_length=20, choices=TOOL_TYPE)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.tool}"