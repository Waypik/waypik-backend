# Waypik Backend API Documentation

## Base URL
```
Development: http://localhost:8000/api/
Production: https://waypik-backend.onrender.com/api/
```

## Authentication
All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

#---

## Authentication Endpoints

### 1. Register (Phone-based)
**Endpoint:** `POST /api/users/register/`  
**Authentication:** Not required  
**Rate Limit:** 5 registrations per hour per IP.  
**Description:** Register a new user with phone number.

**Request Body:**
```json
{
    "username": "+233550000000",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "securepassword123",
    "password2": "securepassword123",
    "email": "john@example.com"  // optional
}
```

**Success Response (201):**
```json
{
    "message": "Account created successfully",
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    },
    "user": {
        "id": 1,
        "phone": "+233550000000",
        "first_name": "John",
        "last_name": "Doe",
        "role": "PASSENGER"
    }
}
```

**Error Response (400):**
```json
{
    "username": ["A user with this phone number already exists."],
    "password2": ["The two password fields didn't match."]
}
```

---

### 2. Login
**Endpoint:** `POST /api/auth/login/`  
**Authentication:** Not required  
**Rate Limit:** 10 attempts per minute per IP.  
**Description:** Login with phone and password to obtain JWT tokens.

**Request Body:**
```json
{
    "phone": "+233550000000",
    "password": "securepassword123"
}
```

**Success Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "pk": 1,
        "phone": "+233550000000",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

**Note:** Access tokens expire in 30 minutes. Refresh tokens expire in 7 days and use rotation (each refresh generates a new refresh token).
- Tokens are also set as HTTP-only cookies in production for enhanced security.

---

### 3. Token Refresh
**Endpoint:** `POST /api/auth/refresh/`  
**Authentication:** Not required (needs refresh token)  
**Description:** Get a new access token using a refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. Logout
**Endpoint:** `POST /api/auth/logout/`  
**Authentication:** Required  
**Description:** Logout and invalidate both access and refresh tokens server-side.

**Success Response (200):**
```json
{
    "detail": "Successfully logged out."
}
```

---

## Social Authentication

### 6. Google Login
**Endpoint:** `POST /api/auth/google/`  
**Authentication:** Not required  
**Description:** Login/Register with Google

**Request Body:**
```json
{
    "access_token": "google_access_token_here"
}
```

### 7. Facebook Login
**Endpoint:** `POST /api/auth/facebook/`  
**Authentication:** Not required  
**Description:** Login/Register with Facebook

**Request Body:**
```json
{
    "access_token": "facebook_access_token_here"
}
```

### 8. Twitter Login
**Endpoint:** `POST /api/auth/twitter/`  
**Authentication:** Not required  
**Description:** Login/Register with Twitter

**Request Body:**
```json
{
    "access_token": "twitter_access_token_here",
    "access_token_secret": "twitter_secret_here"
}
```

---

## User Profile Endpoints

### 5. Get Current User
**Endpoint:** `GET /api/users/me/`  
**Authentication:** Required  
**Description:** Get current authenticated user's profile.

**Success Response (200):**
```json
{
    "id": 1,
    "phone": "+1234567890",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "PASSENGER"
}
```

---

### 6. Update Profile
**Endpoint:** `PATCH /api/users/me/update/`  
**Authentication:** Required  
**Description:** Partial update of user's profile (first_name, last_name, email).

---

### 7. List All Users
**Endpoint:** `GET /api/users/list/`  
**Authentication:** Required (Admin/SuperAdmin only)  
**Description:** Get list of all users. Accessible only to users with ADMIN or SUPERADMIN roles.

---

## Rate Limiting (Throttling)

To protect the API from abuse and brute-force attacks, we implement strict rate limits:

| Scope | Rate | Target Endpoints |
|---|---|---|
| **login** | 10 per minute per IP | `/api/auth/login/` |
| **register** | 5 per hour per IP | `/api/users/register/` |
| **burst** | 60 per minute per user | All authenticated endpoints |
| **sustained** | 1000 per day per user | All authenticated endpoints |

---

## User Roles

The system uses the following roles for access control:
1. **PASSENGER** (default)
2. **DRIVER**
3. **ADMIN** (Transport company administrators)
4. **SUPERADMIN** (System administrators)

---

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message here"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error."
}
```

---

## Phone Number Format

Phone numbers should be in international format:
- **Format:** `+[country_code][number]`
- **Example:** `+1234567890`
- **Length:** 9-15 digits (excluding the + sign)
- **Regex:** `^\+?1?\d{9,15}$`

**Valid Examples:**
- `+1234567890`
- `1234567890`
- `+447911123456`

---

## Testing with cURL

### Register
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

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "+1234567890",
    "password": "securepass123"
  }'
```

### Get Profile (with token)
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Update Profile
```bash
curl -X PATCH http://localhost:8000/api/users/me/update/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny"
  }'
```

---

## Testing with Postman

1. **Import Environment Variables:**
   - `BASE_URL`: `http://localhost:8000/api`
   - `ACCESS_TOKEN`: (will be set after login)

2. **Register a User:**
   - Method: POST
   - URL: `{{BASE_URL}}/users/register/`
   - Body: Raw JSON (see example above)

3. **Login:**
   - Method: POST
   - URL: `{{BASE_URL}}/auth/login/`
   - Body: Raw JSON
   - Save the `access` token from response

4. **Set Authorization:**
   - Go to Authorization tab
   - Type: Bearer Token
   - Token: `{{ACCESS_TOKEN}}`

5. **Test Protected Endpoints:**
   - Use the saved token for all authenticated requests

---

## Next Steps

1. **Add Phone Verification:** Implement SMS OTP verification
2. **Password Reset:** Add password reset via SMS
3. **Rate Limiting:** Prevent brute force attacks
4. **Role-Based Permissions:** Restrict endpoints based on user roles
5. **Social Auth Setup:** Configure provider credentials in Django admin
