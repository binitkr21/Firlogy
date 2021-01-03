from django.shortcuts import render, redirect
from sho.models import Police, Criminal
from user.models import Fir, User, Aadhaar_database,Store,BlockEvidence, BlockTable
from django.db.models import Q
from django.conf import settings
from django.http import FileResponse, Http404
import os
from django.contrib import messages
from . models import Cctv, Sketch
import cv2, numpy
from datetime import datetime
import hashlib
from django.conf import settings
import pandas as pd
import imutils
import pickle

# Create your views here.

def iodashboard(request):
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, "iodashboard.html", {'name':name})

def ioassignedcases(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('iouploadreportview')
    else:
        a = request.session['aadhaar_number']
        cases = Fir.objects.filter(Q(io = a),~Q(status = 'Case Closed'))
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'ioassignedcases.html', {'cases': cases, 'name':name})


def iouploadreportview(request):
    if request.method == 'POST':
        b = 10
    else:
        case_id = request.session['case_id']
        case = Fir.objects.get(case_id=case_id)
        ua = case.aadhaar_number
        abc = Aadhaar_database.objects.get(aadhaar_number=ua)
        u = User.objects.get(aadhaar_number=ua)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'iouploadreportview.html', {'case': case, 'aadhaar': abc, 'user': u, 'case_id': case_id, 'name': name})


def iouploadreport(request):
    if request.method == 'POST':
        file1 = request.FILES.getlist('ffff')


        # file2 = request.FILES.getlist('files')
        # print(file2)
        # for uploaded_file in request.FILES['files']:
        #     print(uploaded_file)
        # print(f)
        # f1= request.FILES.getlist('ffff')
        # print(f1)
        # for uploaded_file in request.FILES.['file']:
        #     print(uploaded_file)

    else:
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, "iouploadreport.html", {'name':name})

def iouploadchargesheet(request):
    if request.method == 'POST':
        case_id = request.session['case_id']
        file = request.FILES.get('ffff',False)
        Fir.objects.filter(case_id=case_id).update(iochargesheet=file,status='Case Closed')
        return  redirect('iouploadreportview')


    else:
        return render(request, "iouploadchargesheet.html")

def iocaserecord(request):
    if request.method == 'POST':
        v = request.POST['sub']
        case_id = v[10:]
        request.session['case_id'] = case_id
        return redirect('iouploadreportview')
    else:
        a = request.session['aadhaar_number']
        cases = Fir.objects.filter(io = a)
        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'iocaserecord.html', {'firs': cases, 'name':name})

def iocasehistoryrecord(request):
    return render(request, "iocasehistoryrecord.html")


def Block1(previous_hash, transaction):
    string_to_hash = transaction+previous_hash
    block_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
    return block_hash

def ionewrecordsupload(request):
    if request.method =='POST':
        a = request.session['aadhaar_number']
        case_id = request.session['case_id']
        evidence = request.FILES.getlist('fir', [])
        for i in evidence:
            s = Store(aadhaar_number=a, file1=i)
            s.save()
        store = Store.objects.filter(aadhaar_number=a)
        s = []
        for st in store:
            s.append(settings.BASE_DIR + 'media_cdn' + st.file1.url)
        x = ''
        for i in s:
            x += i + " "
        temp = ''
        if Fir.objects.get(case_id=case_id).ioevidence != None:
            temp = Fir.objects.get(case_id=case_id).ioevidence
        transaction =temp+x
        now = datetime.now()
        dt_time = now.strftime("%Y-%m-%d %H:%M:%S")
        BlockEvidence(case_id = case_id,date = dt_time,transaction =transaction).save()
        transaction = transaction + dt_time
        if BlockTable.objects.filter(case_id = case_id).exists():
            previoushash =BlockTable.objects.latest('block_id').block
        else:
            previoushash = 'b4bc0b9c68cdcc902bfe86bc6074ca90747977748666bf296fcd9419b4d9b2e0'

        newblock = Block1(previoushash,transaction)
        BlockTable(case_id= case_id, block = newblock).save()

        fir =  Fir.objects.filter(case_id= case_id).update(ioevidence =(temp+x))
        Store.objects.filter(aadhaar_number=a).delete()
        return redirect('iouploadreportview')

    else:
        return render(request, "ionewrecordsupload.html")

def ioviewevidence(request):
    if request.method == 'POST':
        file_name=  request.POST['sub'][7:]
        print(file_name)

        ftype=file_name[-4:]
        if(ftype == '.pdf'):
            path = os.path.join(settings.MEDIA_ROOT, 'evidence/' + file_name)
            return FileResponse(open(path, 'rb'), content_type="application/pdf")
        else:
            path= os.path.join(settings.MEDIA_ROOT, 'evidence/' + file_name)
            img = open(path, 'rb')
            return FileResponse(img)
    else:
        case_id = request.session['case_id']
        evidenceU = []
        evidenceIO = []
        neu = False
        neio = False
        if Fir.objects.get(case_id=case_id).evi != None:
            evidenceU = Fir.objects.get(case_id=case_id).evi
            evidenceU = evidenceU.split(' ')
        else:
            neu = "No evidences uploaded by user"
        if Fir.objects.get(case_id=case_id).ioevidence != None:
            evidenceIO = Fir.objects.get(case_id=case_id).ioevidence[:-1]
            evidenceIO = evidenceIO.split(' ')
        else:
            neio = "You haven't uploaded any evidence"
        eu = []
        eio = []
        mess = '***'
        for ev in evidenceU:
            eu.append(ev[78:])
        for ev in evidenceIO:
            eio.append(ev[78:])
        if BlockEvidence.objects.filter(case_id = case_id).exists():
            b = BlockEvidence.objects.all().order_by('id')
            print(b)
            check = BlockTable.objects.filter(case_id=case_id)
            c =1
            for i in range(len(b)):
                if c == 1:
                    previoushash = 'b4bc0b9c68cdcc902bfe86bc6074ca90747977748666bf296fcd9419b4d9b2e0'
                    c= c+1
                transaction = b[i].transaction + b[i].date
                print(transaction)
                newblock = Block1(previoushash, transaction)
                print(newblock)
                previoushash = newblock
               # print(newblock)
               # print(check[i].block)#e4217e73b2f1f141cb235d1ffc54ff7cbb6edf0c68b0d0db36735ae3fdce0688
                #e75b7d593c6c2b1dcc148b8951f393dfb526639365c8d507ba66c23f23d0ca3c
                if newblock == check[i].block:
                    print(newblock)
                    print(check[i].block)
                else:
                    mess = 'Data discrepancy has been found'


        name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
        return render(request, 'ioviewevidence.html',{'evidencesu':eu, 'evidencesio': eio, 'name':name, 'neu':neu, 'neio':neio,'mess':mess})


def iohelp(request):
    name = Aadhaar_database.objects.get(aadhaar_number=request.session['aadhaar_number']).name
    return render(request, "iohelp.html", {'name':name})

def iocctv(request):
    #result = []
    if request.method == "POST":
        file = request.FILES['ffff']
        print(file)
        a = request.session['aadhaar_number']
        if Cctv.objects.filter(aadhaar_number = a).exists():
            Cctv.objects.filter(aadhaar_number = a).update(file = file)
        else:
            Cctv(aadhaar_number= a,file =file).save()
        c = Cctv.objects.get(aadhaar_number= a).file
        path1 = settings.BASE_DIR+ "/media_cdn/media/cctv/"+str(c)
        print(path1)
        haar_file = (os.path.join(settings.BASE_DIR, 'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
        datasets = 'C:\\Users\\Binit\\Desktop\\face-recognition-master\\face-recognition-master\\dataset'
        (images, labels, names, id) = ([], [], {}, 0)
        for (subdirs, dirs, files) in os.walk(datasets):
            for subdir in dirs:
                names[id] = subdir
                subjectpath = os.path.join(datasets, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + '/' + filename
                    label = id
                    images.append(cv2.imread(path, 0))
                    labels.append(int(label))
                id += 1
        (width, height) = (130, 100)

        (images, labels) = [numpy.array(lists) for lists in [images, labels]]

        model = cv2.face.LBPHFaceRecognizer_create()

        model.train(images, labels)

        face_cascade = cv2.CascadeClassifier(haar_file)
        webcam = cv2.VideoCapture(path1)
        #webcam = cv2.VideoCapture(0)
        result = []
        while True:
            (_, im) = webcam.read()
            if _ == True:
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    prediction = model.predict(face_resize)
                    if prediction[1] < 74:
                        confidence = (prediction[1]) if prediction[1] <= 100.0 else 100.0
                        print("predicted person: {}, confidence: {}%".format(names[prediction[0]].strip(),
                                                                             round((confidence / 74.5) * 100, 2)))
                        temp = names[prediction[0]].strip()
                        c = Criminal.objects.get(aadhaar_number = temp)
                        print(c,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        #messages.info(request, temp)
                        result.append(c)
                    else:
                        print("predicted person: Unknown")
                key = cv2.waitKey(10)
                if key == 27:
                    break
            else:
                print("Frame not found")
                break
        webcam.release()
        cv2.destroyAllWindows()
        #print(result)

        return render(request, 'iocctv.html', {'result':result})
    else:
        return render(request, "iocctv.html")

import numpy as np

outliers = []
def detect_outliers(data):
    threshold = 3
    mean = np.mean(data['Amount'])
    std = np.std(data['Amount'])

    for index, i in enumerate(data['Amount']):
        z_score = (i - mean) / std
        if np.abs(z_score) > threshold:
            outliers.append(data.iloc[index])
    return outliers

def bankdetail(request):
    if request.method == "POST":
        dataset = request.FILES['ffff']
        # dataset = pd.read_excel(
        #     "C:\\Users\\Binit\\PycharmProjects\\Django\\First\\firportal\\static\\files\\bankdata.xlsx")
        Sketch(sid=request.session['aadhaar_number'], sfile=dataset).save()
        dataset = Sketch.objects.get(sid=request.session['aadhaar_number']).sfile.url
        dataset = settings.BASE_DIR + "\\media_cdn" + dataset
        dataset = settings.BASE_DIR + "\\media_cdn" + dataset
        print(dataset,"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        dataset = pd.read_excel(dataset)
        outlier_pt = detect_outliers(dataset)
        transaction_ID = outlier_pt[0]['Transaction ID']
        amount = outlier_pt[0]['Amount']
        date = str(outlier_pt[0]['Date'])[:-9]
        transaction_Type = outlier_pt[0]['Transaction Type']
        account_Number = outlier_pt[0]['Account Number']
        acount_Holder_Name = outlier_pt[0]['Acount Holder Name']
        # bank = [transaction_ID, amount, date, transaction_Type, account_Number, acount_Holder_Name]
        messages.info(request, transaction_ID)
        messages.info(request, amount)
        messages.info(request, date)
        messages.info(request, transaction_Type)
        messages.info(request, account_Number)
        messages.info(request, acount_Holder_Name)
        Sketch.objects.filter(sid=request.session['aadhaar_number']).delete()
        return redirect('bankdetail')
    else:
        return render(request, "bankdetail.html")



def Sketchrecognizer(request):
    if request.method == "POST":
        file = request.FILES['ffff']
        Sketch(sid = request.session['aadhaar_number'], sfile = file).save()
        file = Sketch.objects.get(sid = request.session['aadhaar_number']).sfile.url
        file = settings.BASE_DIR + "/media_cdn/" + file
        print(file)
        image = cv2.imread(file, 1)
        print(image)
        Sketch.objects.filter(sid=request.session['aadhaar_number']).delete()
        print("[INFO] loading face detector...")
        protoPath = "C:\\Users\\Binit\\Downloads\\image recognition in hetrogenous environment\\face-recognition\\face_detection_model\\deploy.prototxt"

        modelPath = "C:\\Users\\Binit\\Downloads\\image recognition in hetrogenous environment\\face-recognition\\face_detection_model\\res10_300x300_ssd_iter_140000.caffemodel"

        detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

        print("[INFO] loading face recognizer...")
        embedder = cv2.dnn.readNetFromTorch(
            "C:\\Users\\Binit\\Downloads\\image recognition in hetrogenous environment\\face-recognition\\openface_nn4.small2.v1.t7")

        recognizer = pickle.loads(open("C:\\Users\\Binit\\Downloads\\image recognition in hetrogenous environment\\face-recognition\\output\\PyPower_recognizer.pickle","rb").read())
        le = pickle.loads(open("C:\\Users\\Binit\\Downloads\\image recognition in hetrogenous environment\\face-recognition\\output\\PyPower_label.pickle","rb").read())

        # image = cv2.imread(
        #     "C:\\Users\\Binit\\Downloads\\image recognition in hetrogenous environment\\face-recognition\\images\\2.jpeg")
        image = imutils.resize(image, width=600)
        (h, w) = image.shape[:2]

        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        detector.setInput(imageBlob)
        detections = detector.forward()

        for i in range(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                if fW < 20 or fH < 20:
                    continue

                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                                 (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]
                text = "{}: {:.2f}%".format(name, proba * 100)
        text = name
        return render(request, 'Sketchrecognizer.html', {'text':text})
    else:
        return render(request, "Sketchrecognizer.html")