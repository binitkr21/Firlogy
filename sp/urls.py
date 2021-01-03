from django.urls import path
from . import views

urlpatterns = [
    path('spdashboard', views.spdashboard, name="spdashboard"),
    path('spassignio', views.spassignio, name="spassignio"),
    path('spiocasedetailview', views.spiocasedetailview, name="spiocasedetailview"),
    path('spselectio', views.spselectio, name="spselectio"),
    path('spcasedetails', views.spcasedetails, name="spcasedetails"),
    path('spsignpad', views.spsignpad, name="spsignpad"),
    path('spotp', views.spotp, name="spotp"),
    path('spnewcases', views.spnewcases, name="spnewcases"),
    path('spreject', views.spreject, name="spreject"),
    path('spfirrecords', views.spfirrecords, name="spfirrecords"),
    path('spfircasedetail', views.spfircasedetail, name="spfircasedetail"),
]
