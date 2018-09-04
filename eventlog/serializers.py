from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Events


class EventsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Events
    fields = ("event", )

class TokenSerializer(serializers.Serializer):
  token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("username", "email")