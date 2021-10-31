from django.urls import path, include

from . import views

app_name = 'AuthApp'
urlpatterns = [
    path('create', views.RegistrationAPIView.as_view(), name="UserCreate"),
]
