from django.urls import path,include
from . import views

urlpatterns = [
    path('rest/v1/calendar/init/', views.GoogleCalendarInitView, name='google_permission'),
    path('rest/v1/calendar/redirect/', views.GoogleCalendarRedirectView, name='google_redirect'),
]
