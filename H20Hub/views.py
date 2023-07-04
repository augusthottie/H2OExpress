from django.utils import timezone
from decimal import Decimal
import random
import string
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views import View
from .models import Meter, WaterPurchase
from .forms import WaterPurchaseForm
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from weasyprint import HTML


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
@login_required
def user_profile_view(request):
    user = request.user
    try:
        meter = Meter.objects.get(user=user)
    except Meter.DoesNotExist:
        # Handle the case where the Meter object does not exist
        meter = None

    purchases = WaterPurchase.objects.filter(user=user)

    context = {
        'user': user,
        'meter': meter,
        'purchases': purchases
    }

    return render(request, 'profile.html', context)

# def generate_token(water_purchase):
#     token = ''.join(random.choices(string.digits, k=20))
#     water_purchase.token = token
#     water_purchase.save()
def generate_token():
    token = ''.join(random.choices(string.digits, k=20))
    return token


def generate_pdf_from_html(html_content, water_purchase):
    water_purchase.vat = water_purchase.vat.quantize(Decimal('0.00'))
    pdf = HTML(string=html_content).write_pdf()
    return pdf

class PurchaseWaterView(View):
    def get(self, request):
        form = WaterPurchaseForm()
        return render(request, 'purchase_water.html', {'form': form})

    def post(self, request):
        form = WaterPurchaseForm(request.POST)
        if form.is_valid():
            amount_paid = form.cleaned_data['amount_paid']
            user = request.user

            units_purchased = amount_paid * Decimal(22.5)  # Example calculation, modify as per your requirement

            # Generate token
            token = generate_token()

            try:
                water_purchase = WaterPurchase(
                    user=user,
                    meter_number=user.meter_number,
                    purchase_date=timezone.localtime(),
                    amount_paid=amount_paid,
                    units_purchased=units_purchased,
                    token=token,
                    vat=Decimal(0.15) * Decimal(amount_paid),  # Convert to Decimal before calculation
                    total_value=Decimal(amount_paid) * Decimal(1.15),  # Convert to Decimal before calculation
                    tax_total=Decimal(0.15) * Decimal(amount_paid),  # Convert to Decimal before calculation
                )

                water_purchase.save()

                # Generate HTML content for the receipt
                template = get_template('receipt.html')
                context = {'purchase': water_purchase}
                html_content = template.render(context)

                # Generate PDF receipt
                pdf = generate_pdf_from_html(html_content, water_purchase)

                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'filename="receipt.pdf"'
                response.write(pdf)

                return response

            except Exception as e:
                # Log the exception details for debugging
                import traceback
                traceback.print_exc()

                # Display a more informative error message to the user
                error_message = f"An error occurred while processing your purchase: {str(e)}"
                return HttpResponse(error_message)

        return render(request, 'purchase_water.html', {'form': form})

def receipt(request):
    user = request.user
    water_purchase = WaterPurchase.objects.filter(user=user).latest('purchase_date')
    context = {'water_purchase': water_purchase}
    return render(request, 'receipt.html', context)
    
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Add success message
            messages.success(request, 'Login successful!')
            return redirect('profile')
        return render(request, 'login.html', {'form': form})
    
class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Retrieve the Meter object for the user
            try:
                meter = Meter.objects.get(user=user)
            except Meter.DoesNotExist:
                # If the Meter object doesn't exist, create it
                meter = Meter(user=user, meter_number=user.meter_number, current_reading=0)
                meter.save()

            login(request, user)
             # Add success message
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('profile')

        return render(request, 'signup.html', {'form': form})
    
def logout_view(request):
    logout(request)
    # Add success message
    messages.success(request, 'Logout successful!')
    return redirect('/')