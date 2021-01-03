from django.shortcuts import render

# Create your views here.
def facilitatordashboard(request):
    return render(request, "facilitatordashboard.html")

def facilitatorassignedcases(request):
    return render(request, "facilitatorassignedcases.html")

def facilitatoruploadreportview(request):
    return render(request, "facilitatoruploadreportview.html")

def facilitatoruploadreport(request):
    return render(request, 'facilitatoruploadreport.html')

def facilitatorcaserecord(request):
    return render(request, "facilitatorcaserecord.html")

def facilitatorcasehistoryrecord(request):
    return render(request, "facilitatorcasehistoryrecord.html")

def facilitatornewrecordsupload(request):
    return render(request, "facilitatornewrecordsupload.html")