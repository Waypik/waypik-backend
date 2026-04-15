"""
Test script for Waypik Backend API
Run this after starting the development server with: python manage.py runserver
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")


def test_registration():
    """Test user registration"""
    url = f"{BASE_URL}/users/register/"
    data = {
        "username": "+233550000000",
        "first_name": "Antigravity",
        "last_name": "Test",
        "password1": "testpass123",
        "password2": "testpass123",
        "email": "antigravity@test.com"
    }

    response = requests.post(url, json=data)
    print_response("1. REGISTRATION TEST", response)
    return response.status_code == 201


def test_login():
    """Test user login"""
    url = f"{BASE_URL}/auth/login/"
    data = {
        "phone": "+233550000000",
        "password": "testpass123"
    }

    response = requests.post(url, json=data)
    print_response("2. LOGIN TEST", response)

    if response.status_code == 200:
        return response.json().get('access')
    return None


def test_protected_endpoint(token):
    """Test protected endpoint with JWT token"""
    url = f"{BASE_URL}/users/protected/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    print_response("3. PROTECTED ENDPOINT TEST", response)
    return response.status_code == 200


def test_get_profile(token):
    """Test get current user profile"""
    url = f"{BASE_URL}/users/me/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    print_response("4. GET PROFILE TEST", response)
    return response.status_code == 200


def test_update_profile(token):
    """Test update user profile"""
    url = f"{BASE_URL}/users/me/update/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "first_name": "Updated",
        "last_name": "Name"
    }

    response = requests.patch(url, json=data, headers=headers)
    print_response("5. UPDATE PROFILE TEST", response)
    return response.status_code == 200


def test_logout(token):
    """Test logout"""
    url = f"{BASE_URL}/auth/logout/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers)
    print_response("6. LOGOUT TEST", response)
    return response.status_code == 200


def test_user_list(token):
    """Test user list endpoint"""
    url = f"{BASE_URL}/users/list/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    print_response("7. USER LIST TEST", response)
    return response.status_code == 200


def test_login_get_all_tokens():
    """Helper to get both access and refresh tokens"""
    url = f"{BASE_URL}/auth/login/"
    data = {
        "phone": "+233550000000",
        "password": "testpass123"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    return None


def test_token_refresh(refresh_token):
    """Test token refresh endpoint"""
    url = f"{BASE_URL}/auth/refresh/"
    data = {
        "refresh": refresh_token
    }
    response = requests.post(url, json=data)
    print_response("8. TOKEN REFRESH TEST", response)
    return response.status_code == 200


def test_forgot_password():
    """Test forgot password endpoint"""
    url = f"{BASE_URL}/auth/password/reset/"
    data = {
        "email": "antigravity@test.com"
    }
    response = requests.post(url, json=data)
    print_response("9. FORGOT PASSWORD TEST", response)
    return response.status_code == 200


def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("WAYPIK BACKEND API TESTS")
    print("="*60)
    print("Make sure the development server is running!")
    print("python manage.py runserver")
    print("="*60)

    # Test 1: Registration
    print("\n[TEST 1] Testing Registration...")
    registration_success = test_registration()

    if not registration_success:
        print("\nWARNING: Registration failed. User might already exist.")
        print("Continuing with login test...")

    # Test 2: Login
    print("\n[TEST 2] Testing Login...")
    access_token = test_login()

    if not access_token:
        print("\nERROR: Login failed! Cannot continue with authenticated tests.")
        return

    print(f"\nSUCCESS: Login successful! Access token obtained.")

    # Test 3: Protected Endpoint
    print("\n[TEST 3] Testing Protected Endpoint...")
    test_protected_endpoint(access_token)

    # Test 4: Get Profile
    print("\n[TEST 4] Testing Get Profile...")
    test_get_profile(access_token)

    # Test 5: Update Profile
    print("\n[TEST 5] Testing Update Profile...")
    test_update_profile(access_token)

    # Test 6: Logout
    print("\n[TEST 6] Testing Logout...")
    test_logout(access_token)

    # Test 7: User List (Admin)
    print("\n[TEST 7] Testing User List...")
    test_user_list(access_token)

    # Test 8: Token Refresh
    # Need a new login to get a fresh refresh token because logout might invalidate it
    print("\n[TEST 8] Testing Token Refresh...")
    tokens = test_login_get_all_tokens()
    if tokens:
        test_token_refresh(tokens.get('refresh'))

    # Test 9: Forgot Password
    print("\n[TEST 9] Testing Forgot Password...")
    test_forgot_password()

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the server!")
        print("Make sure the development server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
