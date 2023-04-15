from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ProtectedView(request):
    user = request.user

    return Response({'message': 'Hello, {}'.format(user.username)})


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:8000/social/github/"
    client_class = OAuth2Client


class GithubConnect(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:8000/social/github/"
    client_class = OAuth2Client
