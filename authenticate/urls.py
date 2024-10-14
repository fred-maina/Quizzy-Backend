from django.urls import path
from .views import register, login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .otp_verification import send_otp, verify_otp  # Import OTP views

urlpatterns = [
    # JWT Token routes
    path('auth/token/', login, name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Registration route
    path('register/', register, name='register'),

    # OTP routes
    path('send-otp/', send_otp, name='send_otp'),  # Send OTP route
    path('verify-otp/', verify_otp, name='verify_otp'),  # Verify OTP route
]
