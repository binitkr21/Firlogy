from django.urls import path, include

from . import views

urlpatterns = [
    path('shodashboard', views.shodashboard, name="shodashboard"),
    path('pendingrequest', views.pendingrequest, name="pendingrequest"),
    path('shocasedetails', views.shocasedetails, name="shocasedetails"),
    path('shosignpad', views.shosignpad, name="shosignpad"),
    path('shocaserecords', views.shocaserecords, name="shocaserecords"),
    path('shootp', views.shootp, name="shootp"),
    path('shoreject', views.shoreject, name="shoreject"),
    path('shofircasedetail', views.shofircasedetail, name="shofircasedetail"),
    path('shoassignfailitator', views.shoassignfailitator, name="shoassignfailitator"),
    path('shofacilitatorcasedetailview', views.shofacilitatorcasedetailview, name="shofacilitatorcasedetailview"),
    path('shoselectfacilitator', views.shoselectfacilitator, name="shoselectfacilitator"),
    path('shofacilitatorrecords', views.shofacilitatorrecords, name="shofacilitatorrecords"),
    path('logout', views.logout, name="logout"),
    path('criminaladd', views.criminaladd, name="criminaladd"),
    path('criminalview', views.criminalview, name="criminalview"),
    path('criminalprofile', views.criminalprofile, name="criminalprofile"),
    path('policeprofile', views.policeprofile, name="policeprofile"),
    path('shoresetpwd', views.shoresetpwd, name="shoresetpwd"),




]
