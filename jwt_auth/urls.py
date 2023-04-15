from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView
)

urlpatterns = [
    path('/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('/blacklist', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('/verify', TokenVerifyView.as_view(), name='token_verify'),
]
