from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework.decorators import api_view
import random
from .models import CustomUser


def send_otp(email, first_name):
    # Generate a random OTP
    otp_code = str(random.randint(100000, 999999))

    # Store OTP in the cache
    cache.set(f'otp_{email}', otp_code, timeout=300)

    # Send OTP email
    subject = 'Your OTP Verification Code'
    html_message = render_to_string('otp_email_template.html', {
        'subscriber_name': first_name,
        'otp_code': otp_code,
    })
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,  # Fallback for non-HTML email clients
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message,
        fail_silently=False,
    )


@api_view(['POST'])
@csrf_exempt  # Use this only if you have to disable CSRF for the view
def verify_otp(request):
    if request.method == "POST":
        data = request.data  # Use request.data to parse JSON automatically
        email = data.get("email")
        entered_otp = data.get("otp")

        # Retrieve the OTP from the cache
        cached_otp = cache.get(f'otp_{email}')

        if cached_otp:
            if entered_otp == cached_otp:
                # OTP is correct, now mark the user as verified
                user = CustomUser.objects.get(email=email)
                if not user.verified:
                    user.verified = True
                    user.save()
                return JsonResponse({"message": "OTP verified successfully! You can now log in."}, status=200)
            else:
                return JsonResponse({"error": "Invalid OTP. Please try again."}, status=400)
        else:
            # OTP expired
            return JsonResponse({"error": "OTP has expired. Please request a new OTP."}, status=400)

    return JsonResponse({"error": "Invalid request."}, status=400)
