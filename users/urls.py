from django.urls import path
from .views import protected_view, register, me

# test urls
urlpatterns = [
    path("protected/", protected_view),
    path("register/", register),
    path("me/", me),
]
