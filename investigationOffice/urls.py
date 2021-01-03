from django.urls import path
from . import views

urlpatterns = [
    path("iodashboard", views.iodashboard, name = "iodashboard"),
    path("ioassignedcases", views.ioassignedcases, name = "ioassignedcases"),
    path("iouploadreportview", views.iouploadreportview, name = "iouploadreportview"),
    path("iouploadreport", views.iouploadreport, name = "iouploadreport"),
    path("iocaserecord", views.iocaserecord, name = "iocaserecord"),
    path("iocasehistoryrecord", views.iocasehistoryrecord, name = "iocasehistoryrecord"),
    path("ionewrecordsupload", views.ionewrecordsupload, name = "ionewrecordsupload"),
    path("iouploadchargesheet", views.iouploadchargesheet, name = "iouploadchargesheet"),
    path("ioviewevidence", views.ioviewevidence, name = "ioviewevidence"),
    path("iohelp", views.iohelp, name = "iohelp"),
    path("iocctv", views.iocctv, name = "iocctv"),
    path("bankdetail", views.bankdetail, name = "bankdetail"),
    path("Sketchrecognizer", views.Sketchrecognizer, name = "Sketchrecognizer"),
]
