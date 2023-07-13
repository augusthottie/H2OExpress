from django.contrib.auth.models import AbstractUser
from django.db import models

class H20User(AbstractUser):
    meter_number = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.username


class Meter(models.Model):
    user = models.OneToOneField(H20User, on_delete=models.CASCADE)
    meter_number = models.PositiveIntegerField(unique=True)
    current_reading = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Meter #{self.meter_number}"

class WaterPurchase(models.Model):
    user = models.ForeignKey(H20User, on_delete=models.CASCADE)
    meter_number = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    token = models.CharField(max_length=20)
    units_purchased = models.DecimalField(max_digits=8, decimal_places=2)
    vat = models.DecimalField(max_digits=8, decimal_places=2)
    total_value = models.DecimalField(max_digits=8, decimal_places=2)
    tax_total = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        # Set the meter number for the water purchase
        self.meter_number = self.user.meter_number

        super().save(*args, **kwargs)

class TransactionHistory(models.Model):
    user = models.ForeignKey(H20User, on_delete=models.CASCADE)
    purchase_id = models.CharField(max_length=100)
    purchase_date = models.DateTimeField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    token = models.CharField(max_length=100)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2)
