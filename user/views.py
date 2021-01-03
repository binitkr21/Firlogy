from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import User, Aadhaar_database, Fir, Evidence, Storage, OTPValidator, Store, Signature, GETVolunteer, FaceRecog, UserNotify
from django.db.utils import DatabaseError
from signapadpy import create_image, Padding
from jsignature.utils import draw_signature
from user.forms import SignatureForm
from sho.models import Police
from django.http import HttpResponse
from django.db.models import Q
from random import randrange
import requests
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
from volunteer.models import Volunteer
from django.conf import settings
from magistrate.models import Magistrate
from django.core.mail import send_mail
from firportal.settings import EMAIL_HOST_USER
from datetime import date


def home(request):
    if request.method == "POST":
        name = request.POST.get('name', 'default')
        phone_number = request.POST.get('phone', 'default')
        email = request.POST.get('email', 'default')
        state = request.POST.get('state', 'default')
        city = request.POST.get('city', 'default')
        address = request.POST.get('address', 'default')
        GETVolunteer(name=name, phone_number=phone_number, email=email, state=state, city=city, address=address,
                     status='Request').save()
        return redirect('home')
    else:
        if request.session.has_key('aadhaar_number'):
            a = request.session['aadhaar_number']
            obj = Aadhaar_database.objects.get(aadhaar_number=a)
            name = obj.name
            user_type = request.session['usertype']
            if user_type == 'user':
                return render(request, 'clientdashboard.html', {'name': name})
            elif user_type == 'sho':
                return render(request, "shodashboard.html", {'name': name})
            elif user_type == 'sp':
                return render(request, "spdashboard.html", {'name': name})
            elif user_type == 'volunteer':
                return render(request, "volunteerdashboard.html", {'name': name})
            elif user_type == 'io':
                return render(request, "iodashboard.html", {'name': name})
            elif user_type == 'magistrate':
                return render(request, "magistratedashboard.html", {'name': name})
        return render(request, 'home.html')


def index(request):
    if request.method == 'POST':
        user_type = request.POST['selector']
        if (user_type != "nothing"):
            phone_number = request.POST['phoneNumber']
            password = request.POST['password']
            if user_type == 'user':
                if User.objects.filter(phone_number=phone_number).exists():
                    data = User.objects.get(phone_number=phone_number)
                    passwordcheck = data.password
                    if password == passwordcheck:
                        request.session['aadhaar_number'] = data.aadhaar_number
                        request.session['usertype'] = 'user'
                        return redirect('clienthome')
                    else:
                        messages.info(request, 'Wrong Password')
                        return redirect('index')
                else:
                    messages.info(request, 'You do not have an account,Create one!!!')
                    return redirect('index')
            elif user_type == 'sho':
                if Police.objects.filter(phone_number=phone_number).exists():
                    if Police.objects.filter(Q(phone_number=phone_number), Q(designation='Sho')).exists():
                        data = Police.objects.get(Q(phone_number=phone_number), Q(designation='Sho'))
                        passwordcheck = data.password
                        if password == passwordcheck:
                            request.session['aadhaar_number'] = data.aadhaar_number
                            request.session['usertype'] = 'sho'
                            return redirect('shodashboard')
                        else:
                            messages.info(request, 'Wrong Password')
                            return redirect('index')
                    else:
                        messages.info(request, 'You do not have Authorization !!!')
                        return redirect('index')
                else:
                    messages.info(request, 'You do not have Authorization !!!')
                    return redirect('index')
            elif user_type == 'sp':
                if Police.objects.filter(phone_number=phone_number).exists():
                    if Police.objects.filter(Q(phone_number=phone_number), Q(designation='Sp')).exists():
                        data = Police.objects.get(Q(phone_number=phone_number), Q(designation='Sp'))
                        passwordcheck = data.password
                        if password == passwordcheck:
                            request.session['aadhaar_number'] = data.aadhaar_number
                            request.session['usertype'] = 'sp'
                            return redirect('spdashboard')
                        else:
                            messages.info(request, 'Wrong Password')
                            return redirect('index')
                    else:
                        messages.info(request, 'You do not have Authorization !!')
                        return redirect('index')
                else:
                    messages.info(request, 'You do not have Authorization !!!')
                    return redirect('index')
            elif user_type == 'io':
                if Police.objects.filter(phone_number=phone_number).exists():
                    if Police.objects.filter(Q(phone_number=phone_number), ~Q(designation='Constable')).exists():
                        data = Police.objects.get(Q(phone_number=phone_number), ~Q(designation='Constable'))
                        passwordcheck = data.password
                        if password == passwordcheck:
                            request.session['aadhaar_number'] = data.aadhaar_number
                            request.session['usertype'] = 'io'
                            return redirect('iodashboard')
                        else:
                            messages.info(request, 'Wrong Password')
                            return redirect('index')
                    else:
                        messages.info(request, 'You do not have Authorization !!')
                        return redirect('index')
                else:
                    messages.info(request, 'You do not have Authorization !!!')
                    return redirect('index')
            elif user_type == 'volunteer':
                if Volunteer.objects.filter(phone_number=phone_number).exists():
                    data = Volunteer.objects.get(phone_number=phone_number)
                    if password == data.password:
                        request.session['aadhaar_number'] = data.aadhaar_number
                        request.session['usertype'] = 'volunteer'
                        return redirect('volunteerdashboard')
                    else:
                        messages.info(request, 'Wrong Password')
                        return redirect('index')
                else:
                    messages.info(request, 'You do not have Authorization !!!')
                    return redirect('index')
            elif user_type == 'magistrate':
                if Magistrate.objects.filter(phone_number=phone_number).exists():
                    data = Magistrate.objects.get(phone_number=phone_number)
                    if password == data.password:
                        request.session['aadhaar_number'] = data.aadhaar_number
                        request.session['usertype'] = 'magistrate'
                        return redirect('magistratedashboard')
                    else:
                        messages.info(request, 'Wrong Password')
                        return redirect('index')
                else:
                    messages.info(request, 'You do not have Authorization !!!')
                    return redirect('index')
        else:
            messages.info(request, 'Select a user type')
            return redirect('index')
    else:
        return render(request, 'index.html')


def logout(request):
    del request.session['usertype']
    del request.session['aadhaar_number']
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        aadhaar_number = request.POST['AadhaarNumber']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(aadhaar_number=aadhaar_number).exists():
            messages.info(request, 'User Already Exists')
            return redirect('register')
        elif not (Aadhaar_database.objects.filter(aadhaar_number=aadhaar_number).exists()):
            messages.info(request, 'Not Registerd In Aadhaar Database')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Already Exists')
            return redirect('register')
        else:
            u = Aadhaar_database.objects.get(aadhaar_number=aadhaar_number)
            p = u.phone_number
            user = User(aadhaar_number=aadhaar_number, email=email, password=password, phone_number=p)
            user.save()
            return redirect('index')
    else:
        return render(request, 'register.html')


def clienthome(request):
    if request.method == "POST":
        return redirect('userprofile')
    else:
        a = request.session['aadhaar_number']
        obj = Aadhaar_database.objects.get(aadhaar_number=a)
        name = obj.name
        noty = UserNotify.objects.filter(Q(aadhaar_number = request.session['aadhaar_number']), ~Q(status = "Registered"))
        return render(request, 'clientdashboard.html', {'name': name, 'noty':noty})


def register_fir(request):
    if request.method == 'POST':
        try:
            request.session['fir_for'] = request.POST.get('inlineRadioOptions','Myself')
            request.session['others_relation'] = request.POST['orelation']
            request.session['o_victim'] = request.POST['ovictim']
            o_gender = request.POST.get('inlineRadioOptions2', False)
            request.session['o_gender'] = o_gender
            request.session['forhname'] = request.POST['forhname']
            request.session['city'] = request.POST['city']
            request.session['police_station'] = request.POST['police_station']
            request.session['date'] = request.POST['date']
            request.session['time'] = request.POST['time']
            request.session['complaint'] = request.POST['complaint']
            request.session['doa'] = request.POST['doa']
            evidence = request.FILES.getlist('evidence', [])
            request.session['status'] = 'Registered'
            a = request.session['aadhaar_number']
            for i in evidence:
                s = Store(aadhaar_number=a, file1=i)
                s.save()
            return redirect('signature')
        except DatabaseError as e:
            messages.info(request, e)
            return redirect('clienthome')
    else:
        if (FaceRecog.objects.filter(aadhaar_number=request.session['aadhaar_number']).exists()):
            FaceRecog.objects.filter(aadhaar_number=request.session['aadhaar_number']).update(known=1, unknown=1,
                                                                                              noone=1)
        else:
            FaceRecog(aadhaar_number=request.session['aadhaar_number'], known=1, unknown=1, noone=1).save()
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'rg.html', {'name':name})


def test(request):
    form = SignatureForm(request.POST or None)
    if form.is_valid():
        signature = form.cleaned_data.get('signature')
        return render(request, 'index.html', {'sig': signature})
    else:
        return render(request, 'test.html')


def clientcaserequest(request):
    if request.method == 'POST':
        b = 10
        v = request.POST['sub']
        a = request.session['aadhaar_number']
        f = Fir.objects.filter(aadhaar_number=a)
        case_id = v[10:]
        request.session['case_id'] = case_id
        return render(request, 'clientcaserequest.html')
    else:
        a = request.session['aadhaar_number']
        f = Fir.objects.filter(aadhaar_number=a)
        return render(request, 'clientcaserequest.html', {'firs': f})


def clientcasedetails(request):
    case_id = request.session['case_id']
    a = request.session['aadhaar_number']
    abc = Aadhaar_database.objects.get(aadhaar_number=a)
    u = User.objects.get(aadhaar_number=a)
    c = Fir.objects.get(case_id=case_id)
    name = abc.name
    if c.paadhaar:
        pa = Aadhaar_database.objects.get(aadhaar_number=c.paadhaar)
        return render(request, 'clientcasedetails.html',
                      {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, "name": name, 'pa':pa})
    else:
        return render(request, 'clientcasedetails.html',{'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, "name": name})


def clientcasehistory(request):
    if request.method == 'POST':
        b = 10
        v = request.POST['sub']
        a = request.session['aadhaar_number']
        f = Fir.objects.filter(aadhaar_number=a)
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('clientcasedetails')
    else:
        a = request.session['aadhaar_number']
        f = Fir.objects.filter(aadhaar_number=a)
        name = Aadhaar_database.objects.get(aadhaar_number=a).name
        return render(request, 'clientcasehistory.html', {'firs': f, "name": name})


def userprofile(request):
    if request.method == 'POST':
        a = request.session['aadhaar_number']
        email = request.POST['email']
        User.objects.filter(aadhaar_number=a).update(email=email)
        return redirect('userprofile')
    else:
        aadhaar_number = request.session['aadhaar_number']
        u = User.objects.get(aadhaar_number=aadhaar_number)
        a = Aadhaar_database.objects.get(aadhaar_number=aadhaar_number)
        return render(request, 'userprofile.html', {"user": u, "aadhaar": a})


def forgotpwd(request):
    return render(request, "forgotpwd.html")


def resetpwd(request):
    if request.method == "POST":
        currentpass = request.POST['currentpass']
        newpass = request.POST['newpass']
        cnfpass = request.POST['cnfpass']
        password = User.objects.get(aadhaar_number=request.session['aadhaar_number']).password
        if (password == currentpass):
            User.objects.filter(aadhaar_number=request.session['aadhaar_number']).update(password=newpass)
            return redirect('index')
        else:
            messages.info(request, 'Wrong Password')
            return redirect('resetpwd')
    else:
        return render(request, "resetpwd.html")


def generate_OTP(uid, phone_number):
    otp = randrange(1111, 9999)
    url = f"https://api.textlocal.in/send/?apiKey=zoL+hAocjgM-w2DUuEnkgYobPgG1jLvUZSlhjpT0cI&sender=TXTLCL&numbers=91{phone_number}&message=Your otp is {otp}"
    #url = f"2R9NaXfyl2E-6PvFUb88Vg3tMMJnDB5R6BoyjAj1GO"
    resp = requests.get(url)
    if resp.json().get('status') == 'success':
        if OTPValidator.objects.filter(aadhaar_number=uid).exists():
            OTPValidator.objects.filter(aadhaar_number=uid).update(otp=otp)
        else:
            OTPValidator(otp=otp, aadhaar_number=uid).save()
    else:
        return 0


def validate_otp(request):
    if request.method == 'POST':
        otp = request.POST['a'] + request.POST['b'] + request.POST['c'] + request.POST['d']
        uid = request.session['aadhaar_number']
        dotp = OTPValidator.objects.get(aadhaar_number=uid).otp
        if dotp == otp:
            fir_for = request.session['fir_for']
            others_relation = request.session['others_relation']
            o_victim = request.session['o_victim']
            o_gender = request.session['o_gender']
            forhname = request.session['forhname']
            city = request.session['city']
            police_station = request.session['police_station']
            date1 = request.session['date']
            time = request.session['time']
            complaint = request.session['complaint']
            doa = request.session['doa']
            status = request.session['status']
            today = date.today()
            today = str(today)
            store = Store.objects.filter(aadhaar_number=uid)
            s = []
            for st in store:
                s.append(settings.BASE_DIR + 'media_cdn' + st.file1.url)
            print(s)
            x = ''
            for i in s:
                x += i + " "
            sa = Fir(aadhaar_number=uid, fir_for=fir_for, o_relation=others_relation, o_victim=o_victim,
                     o_gender=o_gender,
                     fatherorhusbandName=forhname, city=city,
                     police_station=police_station, date=date1, time=time, complaint=complaint, accused_description=doa,
                     status=status,
                     evi=x, curdate = today)
            sa.save()
            Store.objects.filter(aadhaar_number=uid).delete()
            messages.info(request, 'Fir is registered Successfully')
            return redirect('clienthome')
        else:
            messages.info(request, 'Wrong OTP')
            return redirect('validate_otp')
    else:
        return render(request, "validate_otp.html")


def signature(request):
    if request.method == 'POST':
        uid = request.session['aadhaar_number']
        known = FaceRecog.objects.get(aadhaar_number=request.session['aadhaar_number']).known
        unknown = FaceRecog.objects.get(aadhaar_number=request.session['aadhaar_number']).unknown
        noone = FaceRecog.objects.get(aadhaar_number=request.session['aadhaar_number']).noone
        print((known / (known + unknown) * 100), '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        if (noone > 80):
            messages.info(request, 'Failed to detect your face, Please try again !!!')
            return redirect('tryagain')
        elif ((known / (known + unknown) * 100) > 0):
            phone = Aadhaar_database.objects.get(aadhaar_number=uid).phone_number
            generate_OTP(uid, phone)
            return redirect('validate_otp')
        else:
            messages.info(request, 'Failed to recognize your face, Please try again !!!')
            return redirect('tryagain')
    else:
        return render(request, 'signature.html')


def gen(camera, request, aadhaar_number):
    while True:
        cs = camera.get_frame(aadhaar_number)
        frame = cs[0]
        label = cs[1]
        if label == "Unknown":
            unknown = FaceRecog.objects.get(aadhaar_number=aadhaar_number).unknown
            FaceRecog.objects.filter(aadhaar_number=request.session['aadhaar_number']).update(unknown=(unknown + 1))
        elif label == "Multiple":
            print(label)
        elif label == "No One":
            noone = FaceRecog.objects.get(aadhaar_number=aadhaar_number).unknown
            FaceRecog.objects.filter(aadhaar_number=request.session['aadhaar_number']).update(noone=(noone + 1))
        else:
            known = FaceRecog.objects.get(aadhaar_number=aadhaar_number).known
            FaceRecog.objects.filter(aadhaar_number=aadhaar_number).update(known=(known + 1))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    aadhaar_number = request.session['aadhaar_number']
    return StreamingHttpResponse(gen(VideoCamera(), request, aadhaar_number),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def clientfirdownload(request):
    if request.method == "POST":
        v = request.POST['sub']
        a = request.session['aadhaar_number']
        case_id = v[9:]
        c = Fir.objects.get(case_id=case_id)
        abc = Aadhaar_database.objects.get(aadhaar_number=a)
        u = User.objects.get(aadhaar_number=a)
        name = abc.name
        c = Fir.objects.get(case_id=case_id)
        if c.paadhaar:
            pa = Aadhaar_database.objects.get(aadhaar_number=c.paadhaar)
            return render(request, 'clientcasedetails.html',
                      {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, "name": name, "download": True ,"pa":pa})
        else:
            return render(request, 'clientcasedetails.html',
                          {'case': c, 'aadhaar': abc, 'user': u, 'case_id': case_id, "name": name, "download": True})
    else:
        aadhaar_number = request.session['aadhaar_number']
        cases = Fir.objects.filter(aadhaar_number=aadhaar_number)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, "clientfirdownload.html", {'cases': cases, 'name':name})


def getvolunteer(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'default')
        phone_number = request.POST.get('phone', 'default')
        email = request.POST.get('email', 'default')
        state = request.POST.get('state', 'default')
        city = request.POST.get('city', 'default')
        address = request.POST.get('address', 'default')
        GETVolunteer(name=name, phone_number=phone_number, email=email, state=state, city=city, address=address,
                     status='Request').save()
        return redirect('clienthome')
    else:
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'getvolunteer.html', {'name': name})


def useruploadaffidavit(request):
    if request.method == "POST":
        fir = request.FILES['fir']
        case_id = request.session['case_id']
        Fir.objects.filter(case_id=case_id).update(affidavit=fir, status="Requested By Client")
        return redirect('clienthome')
    else:
        return render(request, "useruploadaffidavit.html")

def userseleectmag(request):
    if request == 'POST':
        return redirect('clienthome')
    else:
        mag = Magistrate.objects.all()
        return render(request,'userseleectmag.html',{'mag':mag})

def tryagain(request):
    if request.method == "POST":
        if (FaceRecog.objects.filter(aadhaar_number=request.session['aadhaar_number']).exists()):
            FaceRecog.objects.filter(aadhaar_number=request.session['aadhaar_number']).update(known=1, unknown=1, noone=1)
        else:
            FaceRecog(aadhaar_number=request.session['aadhaar_number'], known=1, unknown=1, noone=1).save()
        return redirect('signature')
    else:
        return render(request, "tryagain.html")


def forgot_password(request):
    if request.method == 'POST':
        aaaa = request.session.get('aadhaar_number')
        user = User.objects.get(aadhaar_number=aaaa)
        eid = user.email
        subject = 'Fir Portal Password change'
        message = 'The link to reset your password is ' + 'http://localhost:8000/reset_password'
        recepient = eid
        send_mail(subject,
                  message, EMAIL_HOST_USER, [recepient], fail_silently=False)
        return render(request, 'email_sent.html', {'recepient': recepient})
    else:
        return render(request, 'forgot_password.html')


def email_sent(request):
    if request.method == 'POST':
        return render(request, 'forgot_password.html')
    else:
        return render(request, 'email_sent.html')


def reset_password(request):
    if request.method == 'POST':
        aaaa = request.session.get('aadhaar_number')
        new = request.POST['npass']
        confirm_new = request.POST['cnpass']
        if new == confirm_new:
            User.objects.filter(aadhaar_number = aaaa).update(password = new)
            return render(request, 'index.html')
        else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('reset_password')
    else:
        return render(request, 'reset_password.html')

