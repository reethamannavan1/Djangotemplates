from django.urls import path
from . import views

urlpatterns = [
    path("tools/", views.tools, name="tools"),
    path("pdf/", views.webpage_to_pdf, name="webpage_pdf"),
    path("image/", views.webpage_to_image, name="webpage_image"),
    path("screenshot/", views.webpage_screenshot, name="webpage_screenshot"),
]