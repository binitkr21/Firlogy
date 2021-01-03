from django.shortcuts import render, redirect
from .models import Police, Criminal
from user.models import Fir, User, Aadhaar_database, OTPValidator, UserNotify
from django.db.models import Q
import random
from django.contrib import messages
from random import randrange
import requests
import numpy as np
import pandas as pd
import re
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
from nltk.stem import WordNetLemmatizer
from django.conf import settings
from datetime import date




def shodashboard(request):
    if request.method == 'POST':
        pass
    else:
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'shodashboard.html', {'name': name})


def pendingrequest(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('shocasedetails')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        police_station = p.police_station
        cases = Fir.objects.filter(Q(police_station=police_station), Q(status="Registered"))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'pendingrequest.html', {'cases': cases, "name": name})


def shocasedetails(request):
    case_id = request.session['case_id']
    case1 = Fir.objects.get(case_id=case_id)
    bhu = case1.curdate
    bhu = bhu.split("-")
    t2 = date(year = int(bhu[0]), month = int(bhu[1]), day = int(bhu[2]))
    t1 = date.today()
    t3 = t1 - t2
    t3 = t3.days
    remaining = 7 - int(t3)
    if remaining < 1:
        Fir.objects.filter(case_id = case_id).update(status = 'Rejected By Sho')
        remaining = "Time limit has already expired , Case has been forwarded to Sp"
    ua = case1.aadhaar_number
    abc = Aadhaar_database.objects.get(aadhaar_number=ua)
    u = User.objects.get(aadhaar_number=ua)
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    case = case1.complaint
    remove_punch = ''
    for i in case:
        if i not in string.punctuation:
            remove_punch += i
    case = remove_punch
    c = re.sub('[^a-zA-Z]', ' ', case)
    c = case.split()
    a = []
    for i in c:
        a.append(i.lower())
    final_word = []
    for i in a:
        if i not in stopwords.words('english'):
            final_word.append(i)
    lemmatizer = WordNetLemmatizer()
    a = []
    for i in final_word:
        a.append(lemmatizer.lemmatize(i))
    ps = PorterStemmer()
    c = [ps.stem(word) for word in a
         if not word in set(stopwords.words('english'))]
    data = pd.read_excel(r"C:\Users\Binit\PycharmProjects\Django\First\firportal\static\files\Newdata.xlsx")

    data = data.values.tolist()
    np.array(data)[:, 1]
    section = []
    for i in c:
        if i in np.array(data)[:, 1]:
            index = np.array(data)[:, 1].tolist().index(i)
            section.append(data[index][2]+" : "+data[index][0])
    output = set(section)
    ua = Fir.objects.get(case_id = case_id).aadhaar_number
    today = date.today()
    if UserNotify.objects.filter(case_id = case_id).exists():
        pass
    else:
        UserNotify(aadhaar_number=ua, case_id= case_id, status = "Registered", user_read = 0, date = today).save()
    if Aadhaar_database.objects.filter(aadhaar_number = case1.aadhaar_number).exists():
        sa = Aadhaar_database.objects.get(aadhaar_number = case1.aadhaar_number)
        return render(request, 'shocasedetails.html',
                      {'case': case1, 'aadhaar': abc, 'user': u, 'case_id': case_id, "name": name, "output": output, "sa":sa, "remaining":remaining})
    else:
        return render(request, 'shocasedetails.html',
                      {'case': case1, 'aadhaar': abc, 'user': u, 'case_id': case_id, "name": name, "output": output, "remaining":remaining})


def generate_OTP(uid, phone_number):
    otp = randrange(1111, 9999)
    #url = f"https://api.textlocal.in/send/?apiKey=2R9NaXfyl2E-6PvFUb88Vg3tMMJnDB5R6BoyjAj1GO&sender=TXTLCL&numbers=91{phone_number}&message=Your otp is {otp}"
    url = f"https://api.textlocal.in/send/?apiKey=zoL+hAocjgM-w2DUuEnkgYobPgG1jLvUZSlhjpT0cI&sender=TXTLCL&numbers=91{phone_number}&message=Your otp is {otp}"

    resp = requests.get(url)
    if resp.json().get('status') == 'success':
        if OTPValidator.objects.filter(aadhaar_number=uid).exists():
            OTPValidator.objects.filter(aadhaar_number=uid).update(otp=otp)
        else:
            OTPValidator(otp=otp, aadhaar_number=uid).save()
    else:
        return 0


def shosignpad(request):
    if request.method == 'POST':
        uid = request.session['aadhaar_number']
        phone = Aadhaar_database.objects.get(aadhaar_number=uid).phone_number
        generate_OTP(uid, phone)
        return redirect('shootp')
    else:
        return render(request, 'shosignpad.html')


def shocaserecords(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('shofircasedetail')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        police_station = p.police_station
        cases = Fir.objects.filter(police_station=police_station)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'shocaserecords.html', {'cases': cases, 'name': name})


def shootp(request):
    if request.method == 'POST':
        otp = request.POST['a'] + request.POST['b'] + request.POST['c'] + request.POST['d']
        uid = request.session['aadhaar_number']
        dotp = OTPValidator.objects.get(aadhaar_number=uid).otp
        if dotp == otp:
            case_id = request.session['case_id']
            f = Fir.objects.get(case_id=case_id)
            p = f.police_station
            fir_id = p[:4] + case_id + str(random.randint(100, 999))
            Fir.objects.filter(case_id=case_id).update(status="Accepted By Sho", fir_id=fir_id, paadhaar = uid)
            today = date.today()
            UserNotify.objects.filter(case_id = case_id).update(status="Accepted By Sho", user_read=1, date=today)
            messages.info(request, 'Fir is registered Successfully')
            return redirect('pendingrequest')
        else:
            messages.info(request, 'Wrong OTP')
            return redirect('shootp')
    else:
        return render(request, "validate_otp.html")


def shoreject(request):
    if request.method == "POST":
        case_id = request.session['case_id']
        Fir.objects.filter(case_id=case_id).update(status="Rejected By Sho")
        today = date.today()
        UserNotify.objects.filter(case_id=case_id).update(status="Rejected By Sho", user_read=1, date=today)
        return redirect('pendingrequest')
    else:
        return render(request, "shoreject.html")


def shofircasedetail(request):
    case_id = request.session['case_id']
    c = Fir.objects.get(case_id=case_id)
    a = c.aadhaar_number
    abc = Aadhaar_database.objects.get(aadhaar_number=a)
    u = User.objects.get(aadhaar_number=a)
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    ra = Aadhaar_database.objects.get(aadhaar_number = request.session['aadhaar_number'])
    return render(request, 'shofircasedetail.html',
                  {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name': name, 'ra':ra})


def shoassignfailitator(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('shofacilitatorcasedetailview')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        police_station = p.police_station
        cases = Fir.objects.filter(Q(police_station=police_station), Q(status="Accepted By Sho"), Q(facilitator=None))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'shoassignfailitator.html', {'cases': cases, 'name': name})


def shofacilitatorcasedetailview(request):
    if request.method == 'POST':
        return redirect('shoselectfacilitator')
    else:
        case_id = request.session['case_id']
        c = Fir.objects.get(case_id=case_id)
        a = c.aadhaar_number
        abc = Aadhaar_database.objects.get(aadhaar_number=a)
        u = User.objects.get(aadhaar_number=a)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        ra = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number'])
        return render(request, 'shofacilitatorcasedetailview.html',
                      {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name': name, 'ra':ra})


def shoselectfacilitator(request):
    if request.method == 'POST':
        aadhaar_number = request.POST['assign'][9:]
        case_id = request.session['case_id']
        Fir.objects.filter(case_id=case_id).update(facilitator=aadhaar_number, io=aadhaar_number)
        return redirect('shoassignfailitator')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        police_station = p.police_station
        officers = Police.objects.filter(Q(police_station=police_station),
                                         ~(Q(designation="Constable")))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, "shoselectfacilitator.html", {'officers': officers, 'name': name})


def shofacilitatorrecords(request):
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    a = request.session['aadhaar_number']
    p = Police.objects.get(aadhaar_number=a)
    police_station = p.police_station
    officers = Police.objects.filter(Q(police_station=police_station),
                                     ~(Q(designation="Constable")))

    return render(request, "shofacilitatorrecords.html", {'name': name, 'officers': officers})


def logout(request):
    del request.session['usertype']
    del request.session['aadhaar_number']
    return render(request, 'home.html')


def criminaladd(request):
    if request.method == 'POST':
        aadhaar_number = request.POST['aadhaar']
        name = request.POST['name']
        crime_type = request.POST['crime']
        police_station = request.POST['police']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        image = request.FILES['image']
        c = Criminal(aadhaar_number=aadhaar_number, name=name, crime_type=crime_type, city=city, state=state,
                     police_station=police_station, address=address, image=image)
        c.save()
        return redirect('shodashboard')
    else:
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'criminaladd.html', {'name': name})


def criminalview(request):
    if request.method == 'POST':
        caadhaar_number = request.POST['view'][7:]
        request.session['caadhaar_number'] = caadhaar_number
        return redirect('criminalprofile')
    else:
        a = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=a)
        police_station = p.police_station
        criminals = Criminal.objects.filter(police_station=police_station)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, "criminalview.html", {'criminals': criminals, 'name': name})


def criminalprofile(request):
    caadhaar_number = request.session['caadhaar_number']
    criminal = Criminal.objects.get(aadhaar_number=caadhaar_number)
    aadhaar = Aadhaar_database.objects.get(aadhaar_number=caadhaar_number)
    return render(request, "criminalprofile.html", {"criminal": criminal, "aadhaar": aadhaar})


def policeprofile(request):
    if request.method == 'POST':
        a = request.session['aadhaar_number']
        email = request.POST['email']
        Police.objects.filter(aadhaar_number=a).update(email=email)
        return redirect('policeprofile')
    else:
        aadhaar_number = request.session['aadhaar_number']
        p = Police.objects.get(aadhaar_number=aadhaar_number)
        a = Aadhaar_database.objects.get(aadhaar_number=aadhaar_number)
        return render(request, 'userprofile.html', {"user": p, "aadhaar": a})


def shoresetpwd(request):
    if request.method == "POST":
        currentpass = request.POST['currentpass']
        newpass = request.POST['newpass']
        cnfpass = request.POST['cnfpass']
        password = Police.objects.get(aadhaar_number=request.session['aadhaar_number']).password
        if (password == currentpass):
            Police.objects.filter(aadhaar_number=request.session['aadhaar_number']).update(password=newpass)
            return redirect('index')
        else:
            messages.info(request, 'Wrong Password')
            return redirect('shoresetpwd')
    else:
        return render(request, "resetpwd.html")
