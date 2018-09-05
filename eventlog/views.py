
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from . import models
from . import serializers

# JWT
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Views
# POST /api/v1/auth/register
class RegisterUsers(generics.CreateAPIView):
  permission_classes = (permissions.AllowAny, )
  def post(self, request, *args, **kwargs):
    user = request.data.get("user")

    if not user["username"] and not user["password"] and not user["email"]:
      return Response(data = {
        "message": "Username, password and email are required"
      }, status = status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
      username = user["username"],
      password = user["password"],
      email = user["email"]
    )

    login(request, user)
    serializer = serializers.TokenSerializer(data = {
      "token": jwt_encode_handler(jwt_payload_handler(user))
    })

    serializer.is_valid()

    return Response({
      'user': serializers.UserSerializer(user).data,
      'token': serializer.data
    })

# POST /api/v1/auth/login
class LoginView(generics.CreateAPIView):
  permission_classes = (permissions.AllowAny, )
  queryset = User.objects.all()

  def post(self, request, *args, **kwargs):
    data = request.data.get("user")
    username = data["username"]
    password = data["password"]
    
    user = authenticate(request, username = username, password = password)

    if user is not None:
      login(request, user)
      serializer = serializers.TokenSerializer(data = {
        "token": jwt_encode_handler(jwt_payload_handler(user))
      })
      serializer.is_valid()
      return Response({
        'user': serializers.UserSerializer(user).data,
        'token': serializer.data
      })
    return Response(status = status.HTTP_401_UNAUTHORIZED)


# GET /api/v1/events
class ListEventsView(generics.ListAPIView):
  queryset = models.Events.objects.all()
  serializer_class = serializers.EventsSerializer
  permission_classes = (permissions.IsAuthenticated, )