from django.shortcuts import render
from .models import AboutIntro, AboutValue

def about(request):
    intro = AboutIntro.objects.first()
 
    values = AboutValue.objects.all()
    return render(request, "about/about.html", {
        "intro": intro,
        "values": values,
    })
