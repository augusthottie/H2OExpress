from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.H20User)
admin.site.register(models.Meter)
admin.site.register(models.WaterPurchase)
admin.site.register(models.TransactionHistory)
