from django.urls import path
from . import views

urlpatterns = [
    path('facilitatordashboard', views.facilitatordashboard, name = "facilitatordashboard"),
    path('facilitatorassignedcases', views.facilitatorassignedcases, name = "facilitatorassignedcases"),
    path('facilitatoruploadreportview', views.facilitatoruploadreportview, name = "facilitatoruploadreportview"),
    path('facilitatoruploadreport', views.facilitatoruploadreport, name = "facilitatoruploadreport"),
    path('facilitatorcaserecord', views.facilitatorcaserecord, name = "facilitatorcaserecord"),
    path('facilitatorcasehistoryrecord', views.facilitatorcasehistoryrecord, name = "facilitatorcasehistoryrecord"),
    path('facilitatornewrecordsupload', views.facilitatornewrecordsupload, name = "facilitatornewrecordsupload"),
]