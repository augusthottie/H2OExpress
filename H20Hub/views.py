from django.utils import timezone
from decimal import Decimal
import random
import string
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from H20Express import settings
from .models import Meter, TransactionHistory, WaterPurchase
from .forms import WaterPurchaseForm
from django.template.loader import get_template
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import braintree

# Configure Braintree
gateway = braintree.BraintreeGateway(
braintree.Configuration.configure(
    braintree.Environment.Sandbox, 
    merchant_id='7x8b8qk6qykgxbhw',
    public_key='j7yfgxr46ryrjbxn',
    private_key='47a88793d6a52f8ac4c1ff56338e1532'
)
)

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


def generate_token():
    token = ''.join(random.choices(string.digits, k=20))
    return token


# def generate_pdf_from_html(html_content, water_purchase):
#     water_purchase.vat = water_purchase.vat.quantize(Decimal('0.00'))
#     pdf = HTML(string=html_content).write_pdf()
#     return pdf

class PurchaseWaterView(View):
    def get(self, request):
        form = WaterPurchaseForm()
        request.session['braintree_client_token'] = braintree.ClientToken.generate()
        return render(request, 'purchase_water.html', {'form': form})

    def post(self, request):
        form = WaterPurchaseForm(request.POST)
        if form.is_valid():
            amount_paid = form.cleaned_data['amount_paid']
            user = request.user

            units_purchased = amount_paid * Decimal(23.5) 

            # Calculate tax amount
            tax_rate = Decimal(0.15)
            tax_amount = amount_paid * tax_rate

            # Calculate total amount after subtracting tax
            total_amount = amount_paid - tax_amount
            total_amount = total_amount.quantize(Decimal('0.00'))

            # Update the amount_paid field of the user
            user.amount_paid += total_amount
            user.save()

            # Convert total amount to string and remove whitespace
            total_amount_str = str(total_amount).strip()
            print(f"Total Amount: {total_amount_str}")

            # Generate token
            token = generate_token()

            try:
                result = braintree.Transaction.sale({
                    'amount': total_amount_str,
                    'payment_method_nonce': request.POST['payment_method_nonce'],
                    'options': {
                        'submit_for_settlement': True
                    }
                })

                if result.is_success:
                    water_purchase = WaterPurchase(
                        user=user,
                        meter_number=user.meter_number,
                        purchase_date=timezone.localtime(),
                        amount_paid=amount_paid,
                        units_purchased=units_purchased,
                        token=token,
                        vat=Decimal(0.15) * Decimal(amount_paid),
                        total_value=Decimal(total_amount) + tax_amount,
                        tax_total=Decimal(0.15) * Decimal(amount_paid),
                    )
                    water_purchase.save()
                    braintree_transaction_id = result.transaction.id

                    # Save the transaction details to the TransactionHistory model
                    transaction_history = TransactionHistory(
                        user=user,
                        purchase_id=water_purchase.id,
                        purchase_date=water_purchase.purchase_date,
                        amount_paid=water_purchase.amount_paid,
                        token=water_purchase.token,
                        vat=water_purchase.vat,
                        total_value=water_purchase.total_value,
                        tax_total=water_purchase.tax_total,
                    )
                    transaction_history.save()
                    # Retrieve the user's transaction history
                    transaction_history = WaterPurchase.objects.filter(user=user)

                    # Redirect to the profile page with transaction history
                    return render(request, 'profile.html', {'purchases': transaction_history})

                else:
                    error_message = f"Transaction failed: {result.message}"
                    return HttpResponse(error_message)

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