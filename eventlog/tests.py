from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Events
from .serializers import EventsSerializer

# tests for views

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_event(event=""):
        if event != "":
            Events.objects.create(event=event)

    def setUp(self):
        # add test data
        self.create_event("Do this")
        self.create_event("Do that")


class GetAllEventsTest(BaseViewTest):

  def test_get_all_events(self):
      # hit the API endpoint
      response = self.client.get(
          reverse("events-all", kwargs={"version": "v1"})
      )
      # fetch the data from db
      expected = Events.objects.all()
      serialized = EventsSerializer(expected, many=True)
      self.assertEqual(response.data, serialized.data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)