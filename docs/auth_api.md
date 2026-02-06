# Authentication API

## WAYPIK Backend Auth – API Contract

### Base URL

http://127.0.0.1:8000/api/auth/

### Register

POST /register/

Body (JSON)

{
  "email": "user@mail.com",
  "password": "password123"
}

### Login

POST /login/

Body

{
  "email": "user@mail.com",
  "password": "password123"
}


### Response

{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}

### Refresh Token

POST /refresh/

{
  "refresh": "JWT_REFRESH_TOKEN"
}

### Get Logged-in User

GET /me/

Headers

Authorization: Bearer JWT_ACCESS_TOKEN


### Response

{
  "email": "user@mail.com",
  "role": "PASSENGER"
}

### Notes

- Store access token securely
- Send Authorization: Bearer <token> on protected requests