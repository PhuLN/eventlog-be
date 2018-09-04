from django.urls import path
from . import views


urlpatterns = [
    path('events/', views.ListEventsView.as_view(), name="events-all")
]