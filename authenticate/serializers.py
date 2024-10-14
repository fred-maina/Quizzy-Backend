from django.apps import apps
from rest_framework import serializers
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


# Use the custom user model dynamically via settings
User = apps.get_model('authenticate', 'CustomUser')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'verified')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Set the 'verified' field to False by default during registration
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.verified = False  # Set the user as not verified on registration
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = custom_authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Check if the user is verified
        if not user.verified:
            raise serializers.ValidationError("User is not verified. Please verify your email.")

        return data
