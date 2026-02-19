import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def create_order(amount_paise):
    data = {
        "amount": int(amount_paise),
        "currency": "INR",
        "payment_capture": 1
    }
    return client.order.create(data)




