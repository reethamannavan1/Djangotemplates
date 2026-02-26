from django.shortcuts import render

from .models import HeroSection


def landing(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    return render(request, "pages/landing.html", {"hero": hero})



from accounts.models import Plan, Subscription


def pricing(request):
    plans = Plan.objects.all().order_by("price")

    user_plan = None
    pending_plan = None

    if request.user.is_authenticated:
        subscription = Subscription.objects.filter(user=request.user).first()

        if subscription:
            user_plan = subscription.plan
            pending_plan = subscription.pending_plan

    return render(request, "pages/pricing.html", {
        "plans": plans,
        "user_plan": user_plan,
        "pending_plan": pending_plan,
    })



#dashboard
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "dashboard/home.html")




#AI Assistant
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from services.ai_service import ask_ai


@csrf_exempt
def ai_assistant(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("prompt")

        result = ask_ai(prompt)

        return JsonResponse({"response": result})