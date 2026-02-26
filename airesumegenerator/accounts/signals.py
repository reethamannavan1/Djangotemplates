from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.utils import timezone
from .models import Plan, Subscription


@receiver(user_signed_up)
def create_subscription_for_google_signup(request, user, **kwargs):
    """
    When user signs up via Google (allauth),
    assign Starter plan + create subscription
    """

    starter = Plan.objects.filter(name__iexact="Starter").first()

    # assign plan to user (temporary until full refactor)
    if starter:
        user.plan = starter
        user.save()

        # create subscription if not exists
        Subscription.objects.get_or_create(
            user=user,
            defaults={
                "plan": starter,
                "billing_cycle": "monthly",
                "start_date": timezone.now(),
                "status": "active",
            },
        )