from django.contrib import admin
from .models import WhyChooseSection, WhyChooseUs,HowVTSWorksSection,HowVTSWorksStep

admin.site.register(WhyChooseUs)
admin.site.register(WhyChooseSection)
admin.site.register(HowVTSWorksSection)
admin.site.register(HowVTSWorksStep)



from .models import StudentProject,StudentStory,CTASection


@admin.register(StudentProject)
class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "student_name", "category", "order")



@admin.register(StudentStory)
class StudentStoryAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")


@admin.register(CTASection)
class CTASectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
