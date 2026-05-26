from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class RegisterSerializer(BaseRegisterSerializer):
    """
    Custom registration serializer for phone-based authentication.
    Handles registration with: first_name, last_name, phone, password
    """
    # Override username field to use phone
    username = serializers.CharField(
        required=True,
        help_text="Phone number",
        label="Phone Number"
    )
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password1 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        help_text="Leave blank if password confirmation is not required"
    )

    class Meta:
        model = User
        fields = (
            'username',  # This will be the phone number
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def validate_username(self, value):
        """
        Validate that the phone number (username) is unique and properly formatted.
        """
        # Check if phone already exists
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists.")

        # Basic phone validation - adjust regex based on your requirements
        # This example accepts: +1234567890, 1234567890, etc.
        phone_validator = RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
        phone_validator(value)

        return value

    def validate(self, data):
        """
        Validate password confirmation if password2 is provided.
        """
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Only validate password match if password2 is provided
        if password2 and password1 != password2:
            raise serializers.ValidationError({
                'password2': "The two password fields didn't match."
            })

        return data

    def get_cleaned_data(self):
        """
        Return cleaned data for user creation.
        This method is called by dj-rest-auth.
        """
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        """
        Create and return a new User instance.
        """
        cleaned_data = self.get_cleaned_data()

        # Create user with phone as the username field
        user = User.objects.create_user(
            phone=cleaned_data['username'],  # Map username to phone
            password=cleaned_data['password1'],
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            email=cleaned_data.get('email', ''),
            role=User.Role.PASSENGER,  # Default role
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model - used for displaying user information.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'created_at',
        )
        read_only_fields = ('id', 'created_at', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    """
    Serializer for current user profile - allows updating own information.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'email',
            'first_name',
            'last_name',
            'role',
        )
        # Phone and role cannot be changed
        read_only_fields = ('id', 'phone', 'role')

    def validate_email(self, value):
        """
        Validate that email is unique if provided.
        """
        user = self.context['request'].user
        if value and User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value


class SocialAuthUserSerializer(serializers.ModelSerializer):
    """
    Serializer for users created via social authentication.
    These users may not have a phone number initially.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
        )
        read_only_fields = ('id', 'email', 'role')

    def validate_phone(self, value):
        """
        Validate phone number if user wants to add it.
        """
        if value:
            # Check if phone already exists
            user = self.context['request'].user
            if User.objects.filter(phone=value).exclude(pk=user.pk).exists():
                raise serializers.ValidationError(
                    "A user with this phone number already exists.")

            # Validate phone format
            phone_validator = RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
            phone_validator(value)

        return value
