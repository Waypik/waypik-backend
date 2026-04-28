from django.contrib import admin
from django.urls import path
from django.urls import include
from users.views import GoogleLogin, FacebookLogin, TwitterLogin

# add JWT urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # This URL is required by dj-rest-auth to generate the password reset link
    # In production, this should point to your Frontend (React/Flutter) password reset page
    path(
        'api/auth/password/reset/confirm/<uidb64>/<token>/',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'
    ),

    path('api/auth/login/', TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Social Authentication Endpoints
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('api/auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),

    # test urls
    path("api/users/", include("users.urls")),
]
