from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer, LoginSerializer
from django.views.decorators.csrf import csrf_exempt
from .otp_verification import send_otp
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import get_user_model


def custom_authenticate(username=None, password=None):
    User = get_user_model()  # Get the custom user model
    try:
        # Attempt to get the user based on the username (or email, if you use email for login)
        user = User.objects.get(username=username)  # Replace 'username' with 'email' if needed
        if user.check_password(password):  # Check if the provided password matches the stored hash
            return user
        else:
            return None  # Password mismatch
    except User.DoesNotExist:
        return None  # User does not exist


CustomUser = get_user_model()


@api_view(['POST'])
@csrf_exempt  # Use this only if you need to disable CSRF for the view
def register(request):
    # Extract necessary data from the request
    data = request.data  # Use request.data to parse the request JSON
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    if not email or not first_name or not last_name:
        return JsonResponse({"error": "Missing required fields."}, status=400)

    # Create the user in the database (or perform any other registration logic)
    user = CustomUser.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    # Call send_otp and pass the user's email and first name
    send_otp(user.email, user.first_name)
    return JsonResponse({"message": "OTP sent successfully"}, status=200)


@csrf_exempt
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Extract username and password from the validated data
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Debugging output
        print(f"Username: {username}")  # Print username
        print(f"Password: {password}")  # Print password

        # Call the custom authenticate function
        user = custom_authenticate(username=username, password=password)

        if user:
            if user.verified:  # Check if the user is verified
                # If user is authenticated and verified, generate the token
                refresh = RefreshToken.for_user(user)
                response = JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
                response.set_cookie('access', str(refresh.access_token), httponly=True)
                print("Login successful")  # Debugging output
                return response
            else:
                print("User is not verified")  # Debugging output
                return Response({"error": "Account not verified. Please verify your email."},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            print("Invalid credentials")  # Debugging output
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    print("Serializer errors:", serializer.errors)  # Debugging output for serializer validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
