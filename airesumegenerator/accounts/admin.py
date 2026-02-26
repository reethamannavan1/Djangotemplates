from django.contrib import admin
from .models import CustomUser, Plan

admin.site.register(CustomUser)
admin.site.register(Plan)


from .models import Subscription

admin.site.register(Subscription)