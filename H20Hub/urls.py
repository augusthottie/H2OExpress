from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='home' ),
    path('profile/',views.user_profile_view, name='profile'),
    path('purchase_water/',views.PurchaseWaterView.as_view(), name='purchase_water'),
    path('receipt/', views.receipt, name='receipt'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('signup/',views.SignupView.as_view(), name='signup'),
    path('logout/',views.logout_view, name='logout'),
]