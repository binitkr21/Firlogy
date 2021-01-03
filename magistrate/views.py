from django.shortcuts import render, redirect
from . models import Magistrate
from user.models import Fir, User, Aadhaar_database, OTPValidator, UserNotify
from django.db.models import Q
import requests
from random import randrange
from django.contrib import messages
from sho.models import Police
from datetime import date



# Create your views here.
def magistratedashboard(request):
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request,"magistratedashboard.html", {'name':name})

def magistrateprofile(request):
    if request.method == 'POST':
        a = request.session['aadhaar_number']
        email = request.POST['email']
        Magistrate.objects.filter(aadhaar_number=a).update(email=email)
        return redirect('magistrateprofile')
    else:
        aadhaar_number = request.session['aadhaar_number']
        p = Magistrate.objects.get(aadhaar_number=aadhaar_number)
        a = Aadhaar_database.objects.get(aadhaar_number=aadhaar_number)
        return render(request, 'userprofile.html', {"user": p, "aadhaar": a})

def magistratepwd(request):
    return render(request,"shoresetpwd.html")

def magistratenewcases(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('magistratecasedetails')
    else:
        a = request.session['aadhaar_number']
        p = Magistrate.objects.get(aadhaar_number=a)
        cases = Fir.objects.filter(Q(status="Requested By Client"), Q(city=p.city))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'magistratenewcases.html', {'cases': cases, 'name':name})

def magistratecasedetails(request):
    if request.method == "POST":
        case_id = request.session['case_id']
        case = Fir.objects.filter(case_id=case_id).update(status = "Rejected By Magistrate")
        today = date.today()
        UserNotify.objects.filter(case_id=case_id).update(status="Rejected By Magistrate", user_read=1, date=today)
        return redirect('magistratenewcases')
    else:
        case_id = request.session['case_id']
        case = Fir.objects.get(case_id=case_id)
        ua = case.aadhaar_number
        abc = Aadhaar_database.objects.get(aadhaar_number=ua)
        u = User.objects.get(aadhaar_number=ua)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'magistratecasedetails.html',
                      {'case': case, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name': name})

def generate_OTP(uid, phone_number):
    otp = randrange(1111, 9999)
    url = f"https://api.textlocal.in/send/?apiKey=zoL+hAocjgM-w2DUuEnkgYobPgG1jLvUZSlhjpT0cI&sender=TXTLCL&numbers=91{phone_number}&message=Your otp is {otp}"
    resp = requests.get(url)
    if resp.json().get('status') == 'success':
        if OTPValidator.objects.filter(aadhaar_number=uid).exists():
            OTPValidator.objects.filter(aadhaar_number=uid).update(otp=otp)
        else:
            OTPValidator(otp=otp, aadhaar_number=uid).save()
    else:
        return 0

def magistratesignpad(request):
    if request.method == 'POST':
        uid = request.session['aadhaar_number']
        phone = Aadhaar_database.objects.get(aadhaar_number=uid).phone_number
        generate_OTP(uid, phone)
        return redirect('magotp')
    else:
        return render(request, 'magistratesignpad.html')

def magotp(request):
    if request.method == 'POST':
        otp = request.POST['a'] + request.POST['b'] + request.POST['c'] + request.POST['d']
        uid = request.session['aadhaar_number']
        dotp = OTPValidator.objects.get(aadhaar_number=uid).otp
        if dotp == otp:
            case_id = request.session["case_id"]
            Fir.objects.filter(case_id=case_id).update(status="Accepted By Magistrate", paadhaar = uid  )
            today = date.today()
            UserNotify.objects.filter(case_id=case_id).update(status="Accepted By Magistrate", user_read=1, date=today)
            return redirect("magistratenewcases")
        else:
            messages.info(request, 'Wrong OTP')
            return redirect('magotp')

    else:
        return render(request, "magotp.html")
#magfirrecords
def magassignio(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('magiocasedetailview')
    else:
        a = request.session['aadhaar_number']
        p = Magistrate.objects.get(aadhaar_number=a)
        city = p.city
        cases = Fir.objects.filter(Q(city=city), Q(status="Accepted By Magistrate"), Q(io=None))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'magassignio.html', {'cases': cases, 'name':name })

def magselectio(request):
    if request.method == 'POST':
        aadhaar_number = request.POST['assign'][9:]
        case_id = request.session['case_id']
        Fir.objects.filter(case_id=case_id).update(io=aadhaar_number, facilitator = 'mag')
        return redirect('magassignio')
    else:
        a = request.session['aadhaar_number']
        p = Magistrate.objects.get(aadhaar_number=a)
        city = p.city
        officers = Police.objects.filter(Q(city=city),
                                         ~Q(designation="Constable"))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, "magselectio.html", {'officers': officers, 'name': name})

def magiocasedetailview(request):
    if request.method == 'POST':
        return redirect('magselectio')
    else:
        case_id = request.session['case_id']
        c = Fir.objects.get(case_id=case_id)
        a = c.aadhaar_number
        abc = Aadhaar_database.objects.get(aadhaar_number=a)
        u = User.objects.get(aadhaar_number=a)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'magiocasedetailview.html', {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name': name})

def magfirrecords(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('magfircasedetail')
    else:
        a = request.session['aadhaar_number']
        p = Magistrate.objects.get(aadhaar_number=a)
        city = p.city
        cases = Fir.objects.filter(Q(city=city), Q(status="Accepted By Magistrate") | Q(status="Rejected By Magistrate") | Q(Q(status="Case Closed"), Q(facilitator = 'mag')))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'magfirrecords.html', {'cases': cases, 'name': name})



def magfircasedetail(request):
    case_id = request.session['case_id']
    c = Fir.objects.get(case_id=case_id)
    a = c.aadhaar_number
    abc = Aadhaar_database.objects.get(aadhaar_number=a)
    u = User.objects.get(aadhaar_number=a)
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, 'magfircasedetail.html',
                  {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name': name})
