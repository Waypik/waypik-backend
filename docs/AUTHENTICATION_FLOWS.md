# Waypik Authentication Flow Diagrams

## 1. Phone-Based Registration & Login Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHONE-BASED AUTHENTICATION                    │
└─────────────────────────────────────────────────────────────────┘

REGISTRATION FLOW:
─────────────────

Client                    Backend                     Database
  │                         │                            │
  │  POST /api/users/register/                          │
  │  {                      │                            │
  │    username: "+123...", │                            │
  │    first_name: "John",  │                            │
  │    last_name: "Doe",    │                            │
  │    password1: "***",    │                            │
  │    password2: "***"     │                            │
  │  }                      │                            │
  ├────────────────────────>│                            │
  │                         │                            │
  │                         │ Validate phone format      │
  │                         │ Check duplicates           │
  │                         │ Validate passwords match   │
  │                         │                            │
  │                         │  Create User               │
  │                         │  - phone: "+123..."        │
  │                         │  - role: PASSENGER         │
  │                         │  - hash password           │
  │                         ├───────────────────────────>│
  │                         │                            │
  │                         │         User Created       │
  │                         │<───────────────────────────┤
  │                         │                            │
  │  201 Created            │                            │
  │  {                      │                            │
  │    message: "Success",  │                            │
  │    user: {...}          │                            │
  │  }                      │                            │
  │<────────────────────────┤                            │
  │                         │                            │


LOGIN FLOW:
───────────

Client                    Backend                     Database
  │                         │                            │
  │  POST /api/auth/login/  │                            │
  │  {                      │                            │
  │    username: "+123...", │                            │
  │    password: "***"      │                            │
  │  }                      │                            │
  ├────────────────────────>│                            │
  │                         │                            │
  │                         │  Find user by phone        │
  │                         ├───────────────────────────>│
  │                         │                            │
  │                         │      User data             │
  │                         │<───────────────────────────┤
  │                         │                            │
  │                         │ Verify password            │
  │                         │ Generate JWT tokens        │
  │                         │ - Access token             │
  │                         │ - Refresh token            │
  │                         │                            │
  │  200 OK                 │                            │
  │  {                      │                            │
  │    access: "eyJ...",    │                            │
  │    refresh: "eyJ...",   │                            │
  │    user: {...}          │                            │
  │  }                      │                            │
  │  + Cookies:             │                            │
  │    - my-app-auth        │                            │
  │    - my-app-refresh-auth│                            │
  │<────────────────────────┤                            │
  │                         │                            │
```

## 2. Social Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOCIAL AUTHENTICATION                         │
│                  (Google / Facebook / Twitter)                   │
└─────────────────────────────────────────────────────────────────┘

Client          Social Provider      Backend              Database
  │                   │                 │                     │
  │ 1. Initiate       │                 │                     │
  │    Social Login   │                 │                     │
  ├──────────────────>│                 │                     │
  │                   │                 │                     │
  │ 2. User Authenticates               │                     │
  │    with Provider  │                 │                     │
  │<─────────────────>│                 │                     │
  │                   │                 │                     │
  │ 3. Access Token   │                 │                     │
  │<──────────────────┤                 │                     │
  │                   │                 │                     │
  │ 4. POST /api/auth/google/           │                     │
  │    { access_token: "..." }          │                     │
  ├────────────────────────────────────>│                     │
  │                   │                 │                     │
  │                   │ 5. Verify Token │                     │
  │                   │<────────────────┤                     │
  │                   │                 │                     │
  │                   │ 6. User Info    │                     │
  │                   ├────────────────>│                     │
  │                   │                 │                     │
  │                   │                 │ 7. Check if user    │
  │                   │                 │    exists (by email)│
  │                   │                 ├────────────────────>│
  │                   │                 │                     │
  │                   │                 │    User found/      │
  │                   │                 │    created          │
  │                   │                 │<────────────────────┤
  │                   │                 │                     │
  │                   │                 │ 8. Generate JWT     │
  │                   │                 │    tokens           │
  │                   │                 │                     │
  │ 9. 200 OK                           │                     │
  │    {                                │                     │
  │      access: "eyJ...",              │                     │
  │      refresh: "eyJ...",             │                     │
  │      user: {...}                    │                     │
  │    }                                │                     │
  │<────────────────────────────────────┤                     │
  │                   │                 │                     │
```

## 3. Profile Update Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                       PROFILE UPDATE                             │
└─────────────────────────────────────────────────────────────────┘

Client                    Backend                     Database
  │                         │                            │
  │  PATCH /api/users/me/update/                        │
  │  Authorization: Bearer <token>                      │
  │  {                      │                            │
  │    first_name: "New"    │                            │
  │  }                      │                            │
  ├────────────────────────>│                            │
  │                         │                            │
  │                         │ Verify JWT token           │
  │                         │ Extract user from token    │
  │                         │                            │
  │                         │ Validate data              │
  │                         │ - Check email uniqueness   │
  │                         │ - Validate phone format    │
  │                         │                            │
  │                         │  Update User               │
  │                         ├───────────────────────────>│
  │                         │                            │
  │                         │      Updated User          │
  │                         │<───────────────────────────┤
  │                         │                            │
  │  200 OK                 │                            │
  │  {                      │                            │
  │    message: "Success",  │                            │
  │    user: {...}          │                            │
  │  }                      │                            │
  │<────────────────────────┤                            │
  │                         │                            │
```

## 4. Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPLETE USER JOURNEY                         │
└─────────────────────────────────────────────────────────────────┘

NEW USER (Phone Auth):
─────────────────────
1. User opens app
2. Clicks "Sign Up"
3. Enters: phone, first_name, last_name, password
4. Backend validates and creates user (role: PASSENGER)
5. User receives JWT tokens
6. User is logged in
7. User can access protected endpoints
8. User can update profile (name, email)
9. User can logout

NEW USER (Social Auth):
──────────────────────
1. User opens app
2. Clicks "Sign in with Google/Facebook/Twitter"
3. Redirected to social provider
4. User authenticates with provider
5. Backend receives access token
6. Backend creates user with email (no phone, no password)
7. User receives JWT tokens
8. User is logged in
9. User can optionally add phone number later
10. User can access protected endpoints

RETURNING USER:
──────────────
1. User opens app
2. Enters phone + password (or uses social login)
3. Backend verifies credentials
4. User receives new JWT tokens
5. User is logged in
6. User can access protected endpoints
```

## 5. Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Frontend   │
│   (Mobile/   │
│     Web)     │
└──────┬───────┘
       │
       │ HTTP/HTTPS
       │ JSON
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│                    Django Backend                         │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │              URL Routing (urls.py)                 │  │
│  └────────────────┬───────────────────────────────────┘  │
│                   │                                       │
│                   ▼                                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Views (views.py)                      │  │
│  │  - register()                                      │  │
│  │  - me()                                            │  │
│  │  - update_profile()                                │  │
│  │  - protected_view()                                │  │
│  └────────────────┬───────────────────────────────────┘  │
│                   │                                       │
│                   ▼                                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │         Serializers (serializers.py)               │  │
│  │  - RegisterSerializer                              │  │
│  │  - UserSerializer                                  │  │
│  │  - UserMeSerializer                                │  │
│  │  - SocialAuthUserSerializer                        │  │
│  └────────────────┬───────────────────────────────────┘  │
│                   │                                       │
│                   ▼                                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │           User Model (models.py)                   │  │
│  │  - UserManager                                     │  │
│  │  - User (AbstractBaseUser)                         │  │
│  │    Fields: phone, email, first_name, last_name,    │  │
│  │            role, is_active, created_at             │  │
│  └────────────────┬───────────────────────────────────┘  │
│                   │                                       │
└───────────────────┼───────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │   PostgreSQL     │
         │    Database      │
         │                  │
         │  Tables:         │
         │  - users_user    │
         │  - auth_*        │
         │  - account_*     │
         │  - socialaccount_*│
         └──────────────────┘
```

## 6. Authentication Middleware Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              REQUEST AUTHENTICATION FLOW                         │
└─────────────────────────────────────────────────────────────────┘

Incoming Request
      │
      ▼
┌─────────────────┐
│  Django         │
│  Middleware     │
│  Stack          │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  JWT Authentication                 │
│  (rest_framework_simplejwt)         │
│                                     │
│  1. Extract token from:             │
│     - Authorization header          │
│     - Cookie (my-app-auth)          │
│                                     │
│  2. Verify token signature          │
│  3. Check expiration                │
│  4. Extract user_id from payload    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Get User from Database             │
│  - Query by user_id                 │
│  - Attach to request.user           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Permission Check                   │
│  - IsAuthenticated?                 │
│  - Role-based permissions?          │
└────────┬────────────────────────────┘
         │
         ├─── ✅ Authorized ──────────> View Function
         │
         └─── ❌ Unauthorized ────────> 401/403 Response
```

## 7. Token Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                      JWT TOKEN LIFECYCLE                         │
└─────────────────────────────────────────────────────────────────┘

Login/Register
      │
      ▼
┌──────────────────────────────────┐
│  Generate Tokens                 │
│  - Access Token (15 min)         │
│  - Refresh Token (7 days)        │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Store Tokens                    │
│  - Client: localStorage/cookies  │
│  - Server: HTTP-only cookies     │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Use Access Token                │
│  - Include in Authorization      │
│  - Valid for 15 minutes          │
└────────┬─────────────────────────┘
         │
         ├──> Token Valid ──────────> Access Granted
         │
         └──> Token Expired ────────┐
                                    │
                                    ▼
                          ┌──────────────────────┐
                          │  Refresh Token       │
                          │  POST /token/refresh/│
                          └──────────┬───────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  New Access Token    │
                          │  (15 min)            │
                          └──────────┬───────────┘
                                     │
                                     └──> Continue Using App
```

---

## Summary

This authentication system provides:

✅ **Dual Authentication Methods**
   - Phone-based (primary)
   - Social auth (Google, Facebook, Twitter)

✅ **Secure Token Management**
   - JWT access tokens (short-lived)
   - Refresh tokens (long-lived)
   - HTTP-only cookies

✅ **Flexible User Model**
   - Supports phone or email
   - Role-based system
   - Profile management

✅ **Production-Ready**
   - Password hashing
   - Token verification
   - Input validation
   - Error handling
