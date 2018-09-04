import json

from django.urls import reverse
from django.contrib.auth.models import User
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

  def login(self, username="", pwd=""):
    url = reverse('login', kwargs={"version": "v1"})
    return self.client.post(url, 
    data = json.dumps({
      "username": username,
      "password": pwd
    }), content_type = "application/json")

  # Also gives token in the header
  def login_client(self, username="", password=""):
    response = self.client.post(
      reverse('create-token'),
      data = json.dumps(
        {
          'username': username,
          'password': password
        }
      ),
      content_type='application/json'
    )
    self.token = response.data['token']
    self.client.credentials(
      HTTP_AUTHORIZATION='Bearer ' + self.token
    )
    self.client.login(username=username, password=password)
    return self.token

  def setUp(self):
    self.user = User.objects.create_superuser(
      username="test",
      email="test@test.com",
      password="test",
    )
    # add test data
    self.create_event("Do this")
    self.create_event("Do that")


class GetAllEventsTest(BaseViewTest):

  def test_get_all_events(self):
    # hit the API endpoint

    self.login_client('test', 'test')

    response = self.client.get(
      reverse("events-all", kwargs={"version": "v1"})
    )
    # fetch the data from db
    expected = Events.objects.all()
    serialized = EventsSerializer(expected, many=True)
    self.assertEqual(response.data, serialized.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

class LoginTest(BaseViewTest):
  def test_valid_credentials(self):
    # Correct login
    response = self.login("test", "test")
    self.assertIn("token", response.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Anon login, unauthorised
    response = self.login("anonymous", "pass")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RegisterUserTest(BaseViewTest):
  def test_register_valid(self):
    url = reverse("register", kwargs={"version": "v1"})
    response = self.client.post(url, data = json.dumps({
      "username": "new",
      "password": "new",
      "email": "new@test.com"
    }), content_type = "application/json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  
  def test_register_invalid(self):
    url = reverse("register", kwargs={"version": "v1"})
    response = self.client.post(url, data = json.dumps({
      "username": "",
      "password": "",
      "email": ""
    }), content_type = "application/json")
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)