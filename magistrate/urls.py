from django.urls import path
from . import views

urlpatterns = [
    path("magistratedashboard", views.magistratedashboard, name = "magistratedashboard"),
    path("magistrateprofile", views.magistrateprofile, name = "magistrateprofile"),
    path("magistratepwd", views.magistratepwd, name = "magistratepwd"),
    path("magistratenewcases", views.magistratenewcases, name = "magistratenewcases"),
    path("magistratecasedetails", views.magistratecasedetails, name = "magistratecasedetails"),
    path("magistratesignpad", views.magistratesignpad, name="magistratesignpad"),
    path("magotp", views.magotp, name="magotp"),
    path("magassignio", views.magassignio, name="magassignio"),
    path("magselectio", views.magselectio, name="magselectio"),
    path("magiocasedetailview", views.magiocasedetailview, name="magiocasedetailview"),
    path("magfirrecords", views.magfirrecords, name="magfirrecords"),
    path("magfircasedetail", views.magfircasedetail, name="magfircasedetail"),

]
