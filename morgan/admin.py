# userinterface/morgan/admin.py
from django.contrib import admin
from .models import Dog, Cart, Order  # Correctly import models from the current app

# Register your models here
admin.site.register(Dog)
admin.site.register(Cart)
admin.site.register(Order)
