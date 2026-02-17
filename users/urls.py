from django.urls import path
from .views import protected_view, register, me, update_profile, UserListView

app_name = 'users'

urlpatterns = [
    # Test endpoint
    path("protected/", protected_view, name="protected"),

    # Registration (alternative to dj-rest-auth registration)
    path("register/", register, name="register"),

    # User profile endpoints
    path("me/", me, name="me"),
    path("me/update/", update_profile, name="update_profile"),

    # User list (admin)
    path("list/", UserListView.as_view(), name="user_list"),
]
