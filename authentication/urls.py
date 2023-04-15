from django.urls import path, include
from .views import ProtectedView, GitHubLogin, GithubConnect
from dj_rest_auth.registration.views import (SocialAccountListView, SocialAccountDisconnectView)
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView,
#     TokenVerifyView,
# )


urlpatterns = [
    # TODO: Remove?
    # path('token/obtain', TokenObtainPairView.as_view(), name='token-obtain'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    # path('token/blacklist', TokenBlacklistView.as_view(), name='token-blacklist'),
    # path('token/verify', TokenVerifyView.as_view(), name='token-verify'),
    # path('register', UserRegistrationView.as_view(), name='register-user'),
    path('', include('dj_rest_auth.urls')),
    path('register/', include('dj_rest_auth.registration.urls')),
    path('social/github/', GitHubLogin.as_view(), name='github_login'),
    path('social/github/connect/', GithubConnect.as_view(), name='github_connect'),
    path('social/', SocialAccountListView.as_view(), name='social_account_list'),
    path('social/<int:pk>/disconnect/', SocialAccountDisconnectView.as_view(), name='social_account_disconnect'),
    path('test-protected-view', ProtectedView, name='test-protected-view'),
]
