from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import H20User, WaterPurchase, Meter

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=255)
    meter_number = forms.IntegerField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=10)

    class Meta(UserCreationForm.Meta):
        model = H20User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'address', 'meter_number', 'first_name', 'last_name','phone_number',)

class WaterPurchaseForm(forms.Form):
    amount_paid = forms.DecimalField(label='Amount Paid', max_digits=8, decimal_places=2)