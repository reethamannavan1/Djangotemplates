from django.shortcuts import render
from .models import Course, Category
from django.db.models import Q 


def courses_page(request):
    categories = Category.objects.all()

    # ⭐ start with all courses
    courses = Course.objects.all()

    # ⭐ SEARCH FILTER
    search_query = request.GET.get("search")
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # ⭐ CATEGORY FILTER
    selected_category = request.GET.get("category")
    if selected_category:
        courses = courses.filter(category__id=selected_category)

    return render(request, "courses/courses.html", {
        "categories": categories,
        "courses": courses,
        "selected_category": selected_category,
        "search_query": search_query, 
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
from .forms import EnrollmentForm


# def course_detail(request, id):
#     course = get_object_or_404(Course, id=id)

#     technologies = course.technologies.all()
#     learning_points = course.learning_points.all()
#     courses = Course.objects.all()

#     form = EnrollmentForm(initial={"course": course})

#     return render(request, "courses/course_detail.html", {
#         "course": course,
#         "technologies": technologies,
#         "learning_points": learning_points,
#          "form": form,
#          "courses": courses,
#     })


from decimal import Decimal
from .payment import create_order
from django.conf import settings


def course_detail(request, id):
    course = Course.objects.get(id=id)
    technologies = course.technologies.all()
    learning_points = course.learning_points.all()
    courses = Course.objects.all()

    fee = course.fee or Decimal("0")
    gst = fee * Decimal("0.18")
    total = fee + gst

    

    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.amount = course.fee
            enrollment.save()
            return redirect("course_detail", id=course.id)
    else:
        form = EnrollmentForm(initial={"course": course})

    return render(request, "courses/course_detail.html", {
        "course": course,
        "technologies": technologies,
        "learning_points": learning_points,
        "courses": courses,
        "form": form,
        "fee": fee,
        "gst": gst,
        "total": total,
         "razorpay_key": settings.RAZORPAY_KEY_ID,
    })





from django.http import JsonResponse

from decimal import Decimal



def create_razorpay_order(request, id):
    course = Course.objects.get(id=id)

    fee = course.fee or Decimal("0")
    gst = fee * Decimal("0.18")
    total = fee + gst

    amount_paise = int(total * 100)

    order = create_order(amount_paise)

    return JsonResponse({
        "order_id": order["id"],
    })





from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def download_invoice(request, id):
    course = Course.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{course.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    # ⭐ simple invoice layout
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Vetri Technology Solutions")

    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Course: {course.title}")
    p.drawString(100, 700, f"Amount: ₹ {course.fee}")

    p.drawString(100, 670, "Thank you for your enrollment!")

    p.showPage()
    p.save()

    return response