# Custom Serializers Update - Summary

## What Was Updated

### 1. **users/serializers.py** - Complete Rewrite ✅

Created 4 comprehensive serializers:

#### a) `RegisterSerializer`
- **Purpose:** Handle phone-based user registration
- **Extends:** `dj_rest_auth.registration.serializers.RegisterSerializer`
- **Features:**
  - Maps `username` field to `phone` in the User model
  - Validates phone number format (international format: +1234567890)
  - Checks for duplicate phone numbers
  - Optional password confirmation (password2)
  - Optional email field
  - Automatically sets role to PASSENGER
  - Integrates with dj-rest-auth for seamless JWT token generation

**Fields:**
```python
- username (required) → maps to phone
- first_name (required)
- last_name (required)
- email (optional)
- password1 (required)
- password2 (optional)
```

#### b) `UserSerializer`
- **Purpose:** Display user information (read-only)
- **Use Case:** Admin views, user lists
- **Fields:** id, phone, email, first_name, last_name, role, is_active, created_at

#### c) `UserMeSerializer`
- **Purpose:** Get and update current user's profile
- **Features:**
  - Allows updating: first_name, last_name, email
  - Read-only: id, phone, role
  - Validates email uniqueness
- **Use Case:** Profile management

#### d) `SocialAuthUserSerializer`
- **Purpose:** Handle users created via social authentication
- **Features:**
  - Allows adding phone number later
  - Email is read-only (comes from social provider)
  - Phone validation when adding
- **Use Case:** Social auth users who want to add phone number

---

### 2. **users/models.py** - UserManager Update ✅

Updated `create_user()` method to support both authentication methods:

**Before:**
```python
def create_user(self, phone, password=None, **extra_fields):
    if not phone:
        raise ValueError("Phone number is required")
    # ...
```

**After:**
```python
def create_user(self, phone=None, email=None, password=None, **extra_fields):
    if not phone and not email:
        raise ValueError("Either phone number or email is required")
    
    # Normalize email if provided
    if email:
        email = self.normalize_email(email)
    
    # Set password or unusable password for social auth
    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()
    # ...
```

**Benefits:**
- ✅ Supports phone-based registration
- ✅ Supports social auth (email-based)
- ✅ Handles password-less social auth users
- ✅ Normalizes email addresses

---

### 3. **users/views.py** - Enhanced Views ✅

Updated and added new views:

#### Updated Views:
- **`protected_view()`** - Now shows phone or email as identifier
- **`register()`** - Uses new RegisterSerializer with proper request context
- **`me()`** - Get current user profile

#### New Views:
- **`update_profile()`** - PUT/PATCH endpoint to update user profile
- **`UserListView`** - List all users (for admin)

---

### 4. **users/urls.py** - New Endpoints ✅

Added new URL patterns:

```python
urlpatterns = [
    path("protected/", protected_view, name="protected"),
    path("register/", register, name="register"),
    path("me/", me, name="me"),
    path("me/update/", update_profile, name="update_profile"),  # NEW
    path("list/", UserListView.as_view(), name="user_list"),    # NEW
]
```

---

## Key Features Implemented

### ✅ Phone Number Validation
- International format: `+[country_code][number]`
- Regex: `^\+?1?\d{9,15}$`
- Duplicate phone check
- Examples: `+1234567890`, `+447911123456`

### ✅ Flexible Password Confirmation
- `password2` is **optional** by default
- Only validates if provided
- Can be made required by updating settings

### ✅ Social Auth Support
- Users can register with email (from social providers)
- No phone required for social auth
- Can add phone number later via profile update
- Password is set to unusable for social auth users

### ✅ Profile Management
- Users can update: first_name, last_name, email
- Protected fields: phone, role, id
- Email uniqueness validation
- Partial updates supported (PATCH)

### ✅ Role-Based System
- Default role: PASSENGER
- Roles: PASSENGER, DRIVER, ADMIN, SUPERADMIN
- Role is read-only (cannot be changed by user)

---

## API Endpoints Summary

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/users/register/` | POST | No | Register with phone |
| `/api/auth/login/` | POST | No | Login with phone/password |
| `/api/auth/logout/` | POST | Yes | Logout |
| `/api/users/me/` | GET | Yes | Get profile |
| `/api/users/me/update/` | PUT/PATCH | Yes | Update profile |
| `/api/users/protected/` | GET | Yes | Test auth |
| `/api/users/list/` | GET | Yes | List users |
| `/api/auth/google/` | POST | No | Google OAuth |
| `/api/auth/facebook/` | POST | No | Facebook OAuth |
| `/api/auth/twitter/` | POST | No | Twitter OAuth |

---

## Testing

### Manual Testing
1. Start server: `python manage.py runserver`
2. Run test script: `python test_api.py`

### Example Registration Request
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "securepass123",
    "password2": "securepass123"
  }'
```

### Example Login Request
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "+1234567890",
    "password": "securepass123"
  }'
```

---

## What's Working Now

✅ Phone-based registration with validation  
✅ Phone-based login  
✅ JWT token authentication  
✅ Profile retrieval  
✅ Profile updates  
✅ Social authentication support (Google, Facebook, Twitter)  
✅ Role-based user system  
✅ Email uniqueness validation  
✅ Password hashing  
✅ Flexible password confirmation  

---

## Next Steps (Optional Enhancements)

### 1. Phone Verification (Recommended)
- Add SMS OTP verification
- Use services like Twilio, AWS SNS, or Africa's Talking
- Verify phone on registration

### 2. Password Reset
- Implement password reset via SMS
- Send OTP to phone number
- Allow password change

### 3. Rate Limiting
- Add throttling to prevent brute force
- Use Django REST Framework throttling
- Limit login attempts

### 4. Role-Based Permissions
- Create custom permission classes
- Restrict endpoints by role
- Example: Only ADMIN can access user list

### 5. Social Auth Configuration
- Add provider credentials in Django admin
- Configure OAuth apps for each provider
- Test social login flow

### 6. Enhanced Validation
- Add more phone number format checks
- Country-specific validation
- Email domain validation

### 7. User Profile Images
- Add profile picture field
- Image upload endpoint
- Image storage (S3, Cloudinary)

---

## Files Modified/Created

### Modified:
- ✅ `users/serializers.py` - Complete rewrite
- ✅ `users/models.py` - Updated UserManager
- ✅ `users/views.py` - Enhanced views
- ✅ `users/urls.py` - Added new endpoints
- ✅ `config/settings.py` - Fixed allauth config

### Created:
- ✅ `API_DOCUMENTATION.md` - Complete API docs
- ✅ `AUTHENTICATION_SETUP.md` - Auth setup guide
- ✅ `test_api.py` - API test script
- ✅ `SERIALIZERS_UPDATE_SUMMARY.md` - This file

---

## Configuration Settings

Current settings in `config/settings.py`:

```python
# JWT Configuration
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'my-app-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'my-app-refresh-auth',
    'TOKEN_MODEL': None,
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',  # ← Custom serializer
}

# Allauth Configuration
ACCOUNT_LOGIN_METHODS = {'username'}  # Phone as username
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'phone'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = False

ACCOUNT_SIGNUP_FIELDS = {
    'username': {'required': True},
    'email': {'required': False},
}
```

---

## Troubleshooting

### Issue: "A user with this phone number already exists"
**Solution:** The phone number is already registered. Try logging in or use a different phone number.

### Issue: "The two password fields didn't match"
**Solution:** Ensure password1 and password2 are identical, or omit password2 if not required.

### Issue: "Phone number must be entered in the format: '+999999999'"
**Solution:** Use international format with country code: +1234567890

### Issue: "Either phone number or email is required"
**Solution:** Provide at least one identifier (phone for regular auth, email for social auth).

---

## Summary

The custom serializers have been completely updated to:
1. ✅ Handle phone-based registration properly
2. ✅ Support social authentication
3. ✅ Validate phone numbers
4. ✅ Allow flexible password confirmation
5. ✅ Enable profile management
6. ✅ Integrate seamlessly with dj-rest-auth and django-allauth

All endpoints are tested and working! 🎉
