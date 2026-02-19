from django.contrib import admin
from .models import Category, Course, CourseTechnology, CourseLearning


admin.site.register(Category)




class CourseTechnologyInline(admin.TabularInline):
    model = CourseTechnology
    extra = 1


class CourseLearningInline(admin.TabularInline):
    model = CourseLearning
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "duration", "is_featured", "order")

    fieldsets = (
        ("Course Card Content", {
            "fields": ("title", "description", "category", "image")
        }),
        ("Detail Page Content", {
            "fields": ("detail_title", "detail_description", "overview")
        }),
        ("Course Info", {
            "fields": ("fee", "duration", "certification", "available_modes")
        }),
        ("Media", {
            "fields": ("preview_image", "preview_video")
        }),
    )

    inlines = [CourseTechnologyInline, CourseLearningInline]



from .models import Enrollment

admin.site.register(Enrollment)
