# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models


# # ⭐ Custom manager
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Email is required")

#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         return self.create_user(email, password, **extra_fields)


# class Plan(models.Model):
#     name = models.CharField(max_length=50)
#     price = models.DecimalField(max_digits=6, decimal_places=2)

#     resume_limit = models.IntegerField(default=1)
#     has_ats = models.BooleanField(default=False)
#     has_cover_letter = models.BooleanField(default=False)
#     advanced_ai = models.BooleanField(default=False)
#     team_features = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name


# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)

#     plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
#     ai_credits = models.IntegerField(default=10)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()  # ⭐ important line

#     def __str__(self):
#         return self.email
    

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# ⭐ Custom manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # ⭐ NULL = unlimited (safe change)
    resume_limit = models.IntegerField(null=True, blank=True)

    has_ats = models.BooleanField(default=False)
    has_cover_letter = models.BooleanField(default=False)
    advanced_ai = models.BooleanField(default=False)
    team_features = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    # ⭐ keep for now (transition period)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    ai_credits = models.IntegerField(default=10)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



#subscription
from django.conf import settings
from django.utils import timezone


class Subscription(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
    ]

    BILLING_CHOICES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)

    billing_cycle = models.CharField(max_length=10, choices=BILLING_CHOICES, default="monthly")

    start_date = models.DateTimeField(default=timezone.now)
    next_billing_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    # ⭐ downgrade scheduling
    pending_plan = models.ForeignKey(
        "Plan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pending_subscriptions"
    )

    # ⭐ Razorpay reference
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"