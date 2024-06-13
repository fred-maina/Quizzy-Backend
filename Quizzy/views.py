from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime

def jwt_auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('access')  # assuming token is stored in cookie

        if not token:
            return redirect('/login/')  # Redirect to login page if token is missing

        try:
            access_token = AccessToken(token)
            current_utc_timestamp = datetime.utcnow().timestamp()

            if access_token['exp'] < current_utc_timestamp:
                raise AccessToken.DoesNotExist

            # Optionally, validate user permissions or other checks here
            # Example: user = User.objects.get(id=access_token['user_id'])

            return view_func(request, *args, **kwargs)

        except Exception as e:
            print(f"JWT verification failed: {e}")
            return render(request, "error.html", {"error_message": "Access denied"})  # Render an error page or handle the error as needed

    return wrapper


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, "login.html")

@jwt_auth_required
def dashboard(request):
    return render(request, "dashboard.html")
