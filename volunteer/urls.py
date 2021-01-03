from django.urls import path
from . import views

urlpatterns = [
    path("volunteerdashboard", views.volunteerdashboard , name = "volunteerdashboard"),
    path("volunteernewcaselist", views.volunteernewcaselist , name = "volunteernewcaselist"),
    path("volunteercasehistoryrecord", views.volunteercasehistoryrecord , name = "volunteercasehistoryrecord"),
    path("volunteerprofile", views.volunteerprofile , name = "volunteerprofile"),
]