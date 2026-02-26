from django.urls import path
from .views import landing, pricing,dashboard,ai_assistant

urlpatterns = [
    path("", landing, name="landing"),
    path("pricing/", pricing, name="pricing"),
    path("dashboard/",dashboard, name="dashboard"),
    path("ai-assistant/", ai_assistant, name="ai_assistant"),
]