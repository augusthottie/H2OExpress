from django.contrib.auth.models import AbstractUser
from django.db import models
import random, string

# class H20User(AbstractUser):
#     meter_number = models.IntegerField(unique=True, null=True)
#     address = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=10)

#     def __str__(self):
#         return self.username

# class Meter(models.Model):
#     user = models.OneToOneField(H20User, on_delete=models.CASCADE)
#     meter_number = models.PositiveIntegerField(unique=True)
#     current_reading = models.DecimalField(max_digits=8, decimal_places=2)

#     def __str__(self):
#         return str(self.meter_number)

#     def __str__(self):
#         return str(self.current_reading)

# class WaterPurchase(models.Model):
#     user = models.ForeignKey(H20User, on_delete=models.CASCADE)
#     meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
#     purchase_date = models.DateTimeField(auto_now_add=True)
#     units_purchased = models.DecimalField(max_digits=8, decimal_places=2)
#     amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
#     token = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return f"Water purchase #{self.id} by {self.user.username}"

#     def save(self, *args, **kwargs):
#         # Generate a random token of 20 numbers
#         if not self.token:
#             self.token = ''.join(random.choices(string.digits, k=20))

#         super().save(*args, **kwargs)

#     def get_unit_amount(self):
#         # Calculate the unit amount including VAT
#         vat_rate = 0.14
#         total_amount = float(self.amount_paid)
#         units_purchased = float(self.units_purchased)
#         unit_amount = total_amount / (1 + vat_rate) / units_purchased
#         return round(unit_amount, 2)


class H20User(AbstractUser):
    meter_number = models.IntegerField(unique=True, null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)

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

