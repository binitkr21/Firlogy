from django.shortcuts import render, redirect
from user.models import GETVolunteer, Aadhaar_database
from .models import Volunteer

# Create your views here.

def volunteerdashboard(request):
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, "volunteerdashboard.html", {'name':name})

def volunteernewcaselist(request):
    if request.method == "POST":
        request_id = request.POST['accept'][9:]
        GETVolunteer.objects.filter (request_id = request_id).update(status = 'Accepted', vid = request.session['aadhaar_number'])
        return redirect('volunteernewcaselist')
    else:
        gv = GETVolunteer.objects.filter(status = "Request")
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, "volunteernewcaselist.html", {'gv':gv, 'name':name})

def volunteercasehistoryrecord(request):
    gv = GETVolunteer.objects.filter(vid = request.session['aadhaar_number'])
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, "volunteercasehistoryrecord.html", {'gv': gv, 'name':name})

def volunteerprofile(request):
    aadhaar_number = request.session['aadhaar_number']
    p = Volunteer.objects.get(aadhaar_number=aadhaar_number)
    a = Aadhaar_database.objects.get(aadhaar_number=aadhaar_number)
    return render(request, 'userprofile.html', {'aadhaar':a, 'user':p})