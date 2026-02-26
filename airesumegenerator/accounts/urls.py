from django.urls import path
from .views import login_view, signup_view, logout_view,change_plan,create_order, payment_success

urlpatterns = [
    path("custom-login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("change-plan/<int:plan_id>/", change_plan, name="change_plan"),
    path("create-order/<int:plan_id>/", create_order, name="create_order"),
    path("payment-success/<int:plan_id>/", payment_success, name="payment_success"),
]