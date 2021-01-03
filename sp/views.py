from django.shortcuts import render, redirect
from sho.models import Police
from user.models import Fir, User, Aadhaar_database, OTPValidator, UserNotify
import random
from django.db.models import Q
from django.contrib import messages
from random import randrange
import requests
from datetime import date


# Create your views here.

def spdashboard(request):
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, "spdashboard.html", {'name':name})


def spassignio(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('spiocasedetailview')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        police_station = p.police_station
        cases = Fir.objects.filter(Q(police_station=police_station), Q(status="Accepted By Sp"), Q(io=None))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'spassignio.html', {'cases': cases, 'name':name })


def spiocasedetailview(request):
    if request.method == 'POST':
        return redirect('spselectio')
    else:
        case_id = request.session['case_id']
        c = Fir.objects.get(case_id=case_id)
        a = c.aadhaar_number
        abc = Aadhaar_database.objects.get(aadhaar_number=a)
        u = User.objects.get(aadhaar_number=a)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'spiocasedetailview.html', {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name': name})


def spselectio(request):
    if request.method == 'POST':
        aadhaar_number = request.POST['assign'][9:]
        case_id = request.session['case_id']
        Fir.objects.filter(case_id=case_id).update(io=aadhaar_number)
        return redirect('spassignio')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        city = p.city
        officers = Police.objects.filter(Q(city=city),
                                         ~(Q(designation="Constable") ))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, "spselectio.html", {'officers': officers, 'name': name})


def spcasedetails(request):
    case_id = request.session['case_id']
    case = Fir.objects.get(case_id=case_id)
    ua = case.aadhaar_number
    abc = Aadhaar_database.objects.get(aadhaar_number=ua)
    u = User.objects.get(aadhaar_number=ua)
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, 'spcasedetails.html', {'case': case, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name':name})


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


def spsignpad(request):
    if request.method == 'POST':
        uid = request.session['aadhaar_number']
        phone = Aadhaar_database.objects.get(aadhaar_number=uid).phone_number
        generate_OTP(uid, phone)
        return redirect('spotp')
    else:
        return render(request, 'spsignpad.html')


def spotp(request):
    if request.method == 'POST':
        otp = request.POST['a'] + request.POST['b'] + request.POST['c'] + request.POST['d']
        uid = request.session['aadhaar_number']
        dotp = OTPValidator.objects.get(aadhaar_number=uid).otp
        if dotp == otp:
            case_id = request.session["case_id"]
            Fir.objects.filter(case_id=case_id).update(status="Accepted By Sp", paadhaar = uid)
            today = date.today()
            UserNotify.objects.filter(case_id=case_id).update(status="Accepted By Sp", user_read=1, date=today)
            return redirect("spnewcases")
        else:
            messages.info(request, 'Wrong OTP')
            return redirect('spotp')
    else:
        return render(request, "spotp.html")


def spnewcases(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('spcasedetails')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        cases = Fir.objects.filter(Q(status="Rejected By Sho"), Q(city=p.city))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'spnewcases.html', {'cases': cases, 'name':name})


def spreject(request):
    if request.method == 'POST':
        case_id = request.session['case_id']
        Fir.objects.filter(case_id=case_id).update(status="Rejected By Sp")
        today = date.today()
        UserNotify.objects.filter(case_id=case_id).update(status="Rejected By Sp", user_read=1, date=today)
        return redirect('spnewcases')
    else:
        return render(request, "spreject.html")


def spfirrecords(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('spfircasedetail')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        city = p.city
        cases = Fir.objects.filter(Q(city=city), Q(facilitator=None))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'spfirrecords.html', {'cases': cases, 'name':name})


def spfircasedetail(request):
    case_id = request.session['case_id']
    c = Fir.objects.get(case_id=case_id)
    a = c.aadhaar_number
    abc = Aadhaar_database.objects.get(aadhaar_number=a)
    u = User.objects.get(aadhaar_number=a)
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, 'spfircasedetail.html', {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name':name})
