from rest_framework import generics
from . import models
from . import serializers

# Create your views here.
class ListEventsView(generics.ListAPIView):
  queryset = models.Events.objects.all()
  serializer_class = serializers.EventsSerializer