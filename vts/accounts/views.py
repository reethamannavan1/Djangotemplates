from django.shortcuts import render

from .models import WhyChooseUs, WhyChooseSection, HowVTSWorksSection, HowVTSWorksStep
from .models import StudentProject,StudentStory,CTASection
from courses.models import Course



def home(request):
    section = WhyChooseSection.objects.first()
    features = WhyChooseUs.objects.all()
    works_section = HowVTSWorksSection.objects.first()
    steps = HowVTSWorksStep.objects.all()

    projects = StudentProject.objects.all()[:3]
    stories = StudentStory.objects.all()
    cta = CTASection.objects.first()

    featured_courses = Course.objects.filter(is_featured=True)[:3]

    return render(request, "home.html", {
        "section": section,
        "features": features,
        "works_section": works_section,
        "steps": steps,
        "projects": projects,
        "stories":stories,
        "cta":cta,
        "featured_courses":featured_courses,
    })


