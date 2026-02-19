from django.shortcuts import render
from django.contrib import messages
from courses.models import Course


def contact_page(request):

    courses = Course.objects.all()

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if not name or not email or not phone:
            messages.error(request, "Please fill all required fields.")
        else:
            messages.success(request, "Enquiry submitted successfully!")

    return render(request, "contact/contact.html", {"courses": courses})
