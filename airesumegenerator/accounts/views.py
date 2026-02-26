from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import LoginForm, SignupForm
from .models import Plan, Subscription


#downgrade
from django.utils import timezone


def apply_pending_downgrade(user):
    subscription = Subscription.objects.filter(user=user).first()

    if not subscription:
        return

    # if pending downgrade exists
    if subscription.pending_plan and subscription.next_billing_date:

        # billing date reached
        if timezone.now() >= subscription.next_billing_date:
            subscription.plan = subscription.pending_plan
            subscription.pending_plan = None
            subscription.save()

            user.plan = subscription.plan
            user.save()



#login

def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                Subscription.objects.get_or_create(
                    user=user,
                    defaults={"plan": user.plan}
    )
                apply_pending_downgrade(user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid email or password")

    return render(request, "accounts/login.html", {"form": form})




#signup
# from .forms import SignupForm
# from django.contrib.auth import login, get_user_model
# from .models import Plan


# def signup_view(request):
#     form = SignupForm()

#     if request.method == "POST":
#         form = SignupForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data["email"]
#             password = form.cleaned_data["password"]

#             starter = Plan.objects.filter(name__iexact="Starter").first()

#             User = get_user_model()
#             user = User.objects.create_user(email=email, password=password, plan=starter)

#             login(request, user)
#             return redirect("/")

#     return render(request, "accounts/signup.html", {"form": form})



from .forms import SignupForm
from django.contrib.auth import login, get_user_model
from .models import Plan, Subscription
from django.utils import timezone


def signup_view(request):
    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            starter = Plan.objects.filter(name__iexact="Starter").first()

            User = get_user_model()
            user = User.objects.create_user(email=email, password=password, plan=starter)

            # ⭐ CREATE SUBSCRIPTION
            Subscription.objects.create(
                user=user,
                plan=starter,
                billing_cycle="monthly",
                start_date=timezone.now(),
                status="active"
            )

            login(request, user)
            return redirect("/")

    return render(request, "accounts/signup.html", {"form": form})




from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return render(request, "accounts/logout_success.html")



#pricing
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Plan, Subscription
from django.contrib import messages
from datetime import timedelta


@login_required
def change_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    subscription, created = Subscription.objects.get_or_create(
    user=request.user,
    defaults={"plan": request.user.plan}
)

    # Upgrade
    if plan.price > subscription.plan.price:
        subscription.plan = plan
        subscription.pending_plan = None
        subscription.save()

        request.user.plan = plan
        request.user.save()

        messages.success(request, f"Upgraded to {plan.name}")

    # Downgrade
    elif plan.price < subscription.plan.price:
        subscription.pending_plan = plan
        subscription.next_billing_date = timezone.now() + timedelta(days=30)
        subscription.save()

        messages.info(request, f"Downgrade to {plan.name} scheduled")

    return redirect("pricing")





#paymentintegration

import razorpay
from django.conf import settings
from django.http import JsonResponse


@login_required
def create_order(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount = int(plan.price * 100)  # paisa

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return JsonResponse({
        "order_id": order["id"],
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID,
        "plan_id": plan.id,
        "plan_name": plan.name
    })



#paymentsuccess
@login_required
def payment_success(request, plan_id):
    payment_id = request.GET.get("payment_id")

    plan = get_object_or_404(Plan, id=plan_id)

    subscription, _ = Subscription.objects.get_or_create(user=request.user)

    # ⭐ activate plan
    subscription.plan = plan
    subscription.razorpay_payment_id = payment_id
    subscription.pending_plan = None
    subscription.save()

    request.user.plan = plan
    request.user.save()

    messages.success(request, f"Payment successful. Upgraded to {plan.name}")

    return redirect("pricing")