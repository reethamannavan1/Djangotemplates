from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback


def feedback_view(request):

    if request.method == "POST":
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")

        # Validation
        if not subject:
            messages.error(request, "Subject is required")
            return redirect("feedback")

        if not message_text:
            messages.error(request, "Message is required")
            return redirect("feedback")

        # Save feedback
        Feedback.objects.create(
            user=request.user,
            subject=subject,
            message=message_text
        )

        messages.success(request, "Thanks for your feedback!")
        return redirect("feedback")

    return render(request, "feedback/feedback.html")