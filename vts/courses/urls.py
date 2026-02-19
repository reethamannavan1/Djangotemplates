from django.urls import path
from .views import courses_page, course_detail,create_razorpay_order

urlpatterns = [
    path('', courses_page, name='courses'),
    path('<int:id>/', course_detail, name='course_detail'),
    path("create-order/<int:id>/", create_razorpay_order, name="create_order"),

]
