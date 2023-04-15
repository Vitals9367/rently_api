from django.urls import path
from .views import UserRegistrationView, ProtectedView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView
)
from rest_framework_social_oauth2.views import (
    ConvertTokenView,
    TokenView,
)

urlpatterns = [
    path('token/obtain', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/blacklist', TokenBlacklistView.as_view(), name='token-blacklist'),
    path('token/verify', TokenVerifyView.as_view(), name='token-verify'),
    path('token/convert-token/', ConvertTokenView.as_view(), name='convert-token'),
    path('token/', TokenView.as_view(), name='token'),
    path('test-protected-view/', ProtectedView, name='test-protected-view'),
    path('register/', UserRegistrationView.as_view(), name='register-user'),
]
