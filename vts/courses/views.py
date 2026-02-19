from django.shortcuts import render
from .models import Course, Category


def courses_page(request):
    categories = Category.objects.all()
    selected_category = request.GET.get("category")

    if selected_category:
        courses = Course.objects.filter(category__id=selected_category)
    else:
        courses = Course.objects.all()

    return render(request, "courses/courses.html", {
        "categories": categories,
        "courses": courses,
        "selected_category": selected_category,
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




