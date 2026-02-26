from django.urls import path
from . import views

urlpatterns = [
    path("", views.resume_home, name="resume_home"),
    # resumes/urls.py
    path("optimizer/", views.resume_optimizer, name="resume_optimizer"),
    path("download-pdf/", views.download_optimized_resume_pdf, name="download-optimized-resume-pdf"),
    path("templates/", views.templates, name="templates"),
    path("create/", views.create_resume, name="create-resume"),

    path("list/", views.resume_list, name="resume-list"),
    path("delete/<int:pk>/", views.delete_resume, name="delete-resume"),
    

    #coverletter
    path("cover-letter/", views.cover_letter, name="cover_letter"),
    path("download-cover-letter/", views.download_cover_letter_pdf, name="download_cover_letter_pdf"),


    #templates
    path("templates/", views.templates, name="templates"),
path("template-preview/<int:pk>/", views.preview_template, name="preview_template"),
path("use-template/<int:pk>/", views.use_template, name="use_template"),

]