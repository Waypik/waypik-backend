# Waypik Backend Authentication Setup

## Overview
This document explains the authentication configuration for the Waypik transport application.

## Authentication Methods

### 1. **Phone-Based Authentication** (Primary)
- **Signup**: Users provide `first_name`, `last_name`, and `phone`
- **Login**: Users login with `phone` + `password`
- After login, users confirm their information (first_name, last_name)

### 2. **Social Authentication** (Alternative)
Supported providers:
- Google
- Facebook
- Twitter (X)
- Apple (configured but requires provider setup)

## Current Configuration

### User Model (`users/models.py`)
```python
class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PASSENGER)
    
    USERNAME_FIELD = "phone"  # Phone is used for authentication
```

### Django Settings (`config/settings.py`)

#### Installed Apps
```python
INSTALLED_APPS = [
    # ... Django apps ...
    'rest_framework',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.apple',  # Requires additional setup
    'users',
    'transport',
    'bookings',
]
```

#### Authentication Configuration
```python
# JWT Configuration
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-app-refresh-auth'

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'my-app-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'my-app-refresh-auth',
    'TOKEN_MODEL': None,
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
}

# Django Allauth Configuration for Phone-based Authentication
ACCOUNT_LOGIN_METHODS = {'username'}  # Phone is treated as username
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'phone'  # Use phone as the username field
ACCOUNT_EMAIL_VERIFICATION = 'none'  # No email verification needed
ACCOUNT_UNIQUE_EMAIL = False  # Email doesn't need to be unique

ACCOUNT_SIGNUP_FIELDS = {
    'username': {'required': True},  # Maps to 'phone' field
    'email': {'required': False},
}
```

## What's Correct ✅

1. **Phone as Primary Identifier**: The `USERNAME_FIELD = "phone"` correctly sets phone as the login credential
2. **JWT Authentication**: Properly configured for token-based auth
3. **Social Auth Providers**: Google, Facebook, and Twitter are installed
4. **Custom User Model**: Extends `AbstractBaseUser` with custom fields
5. **Role-Based Access**: User model includes role field (PASSENGER, DRIVER, ADMIN, SUPERADMIN)

## What Was Missing/Fixed ❌➡️✅

### 1. **Password Fields Configuration**
- **Issue**: Settings had `ACCOUNT_SIGNUP_FIELDS = ['email', 'password1*', 'password2*']` which was:
  - Incorrect for phone-based auth
  - Using deprecated format
  - Conflicting with the user model
- **Fix**: Updated to use phone (username) instead of email

### 2. **Allauth Settings**
- **Issue**: Using deprecated settings like `ACCOUNT_AUTHENTICATION_METHOD`, `ACCOUNT_USERNAME_REQUIRED`, `ACCOUNT_EMAIL_REQUIRED`
- **Fix**: Migrated to new format using `ACCOUNT_LOGIN_METHODS` and `ACCOUNT_SIGNUP_FIELDS` dictionary

### 3. **User Model Fields**
- **Issue**: `phone` was required but should be optional for social auth users
- **Fix**: Made both `phone` and `email` nullable to support both auth methods:
  - Phone auth users: have phone, may not have email
  - Social auth users: have email, may not have phone

### 4. **Custom Registration Serializer**
- **Added**: `'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer'` to handle custom signup flow

## API Endpoints

### Registration & Login
- `POST /api/auth/registration/` - Register with phone, first_name, last_name, password
- `POST /api/auth/login/` - Login with phone and password
- `POST /api/auth/logout/` - Logout (invalidate token)

### Social Authentication
- `/api/auth/google/` - Google OAuth
- `/api/auth/facebook/` - Facebook OAuth
- `/api/auth/twitter/` - Twitter OAuth

### User Management
- `GET /api/users/me/` - Get current user info
- `GET /api/users/protected/` - Test protected endpoint

## Next Steps / TODO

### 1. **Custom Serializers**
Update `users/serializers.py` to handle:
- Phone-based registration (first_name, last_name, phone, password)
- Optional email from social auth
- Password confirmation if needed

### 2. **Social Auth Setup**
Configure each provider in Django admin:
- Google: Client ID, Secret
- Facebook: App ID, Secret
- Twitter: API Key, Secret
- Apple: Service ID, Team ID, Key ID, Private Key

### 3. **Phone Verification**
Consider adding:
- SMS verification for phone numbers
- OTP (One-Time Password) for login
- Phone number validation

### 4. **Custom User Manager**
The `UserManager.create_user()` currently requires phone. Update to:
```python
def create_user(self, phone=None, email=None, password=None, **extra_fields):
    if not phone and not email:
        raise ValueError("Either phone or email is required")
    # ... handle both cases
```

### 5. **Admin Panel**
Update `users/admin.py` to display phone instead of just email:
```python
list_display = ("phone", "email", "role", "is_active", "is_staff", "created_at")
search_fields = ("phone", "email", "first_name", "last_name")
```

## Known Warnings

### Deprecation Warnings (from dj-rest-auth library)
These are from the `dj-rest-auth` package itself and will be fixed in future versions:
```
UserWarning: app_settings.USERNAME_REQUIRED is deprecated
UserWarning: app_settings.EMAIL_REQUIRED is deprecated
```

### Configuration Warning
```
(account.W001) ACCOUNT_LOGIN_METHODS conflicts with ACCOUNT_SIGNUP_FIELDS
```
This is expected when using custom signup fields. It's a warning, not an error.

## Testing Checklist

- [ ] Phone-based registration works
- [ ] Phone-based login works
- [ ] JWT tokens are issued correctly
- [ ] Social auth (Google) works
- [ ] Social auth (Facebook) works
- [ ] Social auth (Twitter) works
- [ ] Users can update their profile
- [ ] Password reset works (if implemented)
- [ ] Role-based permissions work

## Security Considerations

1. **Phone Number Validation**: Implement proper phone number format validation
2. **Rate Limiting**: Add rate limiting to prevent brute force attacks
3. **SMS Verification**: Implement OTP verification for phone numbers
4. **HTTPS Only**: Ensure all auth endpoints use HTTPS in production
5. **Token Expiry**: Configure appropriate JWT token expiration times
6. **Password Strength**: Enforce strong password requirements
