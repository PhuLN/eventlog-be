from django.urls import path
from .views import ListEventsView, LoginView, RegisterUsers

urlpatterns = [
    path('events/', ListEventsView.as_view(), name="events-all"),
    path('auth/login/', LoginView.as_view(), name = "login"),
    path('auth/register/', RegisterUsers.as_view(), name = "register")
]