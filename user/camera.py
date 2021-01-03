# import cv2,os
# from .models import CameraUser
#
# from django.conf import settings
# face_detection_videocam = cv2.CascadeClassifier(os.path.join(
# 			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
# face_detection_webcam = cv2.CascadeClassifier(os.path.join(
# 			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
#
# class VideoCamera(object):
# 	def __init__(self):
# 		self.video = cv2.VideoCapture(0)
#
# 	def __del__(self):
# 		self.video.release()
#
# 	def get_frame(self):
# 		cams = CameraUser.objects.all()
# 		images = []
# 		for cam in cams:
# 			images.append(cv2.imread(cam.img.url, 1))
# 		success, image = self.video.read()
# 		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
# 		# so we must encode it into JPEG in order to correctly display the
# 		# video stream.
#
# 		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
# 		for (x, y, w, h) in faces_detected:
# 			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
# 		frame_flip = cv2.flip(image,1)
# 		ret, jpeg = cv2.imencode('.jpg', frame_flip)
# 		return jpeg.tobytes()


# import cv2, os
# import numpy as np
# from django.conf import settings
# from .models import CameraUser
#
# face_detection_videocam = cv2.CascadeClassifier(os.path.join(
#     settings.BASE_DIR, 'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
#
#
# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#
#     def __del__(self):
#         self.video.release()
#
#     def get_prediction(self, gray, faces):
#         (width, height) = (130, 100)
#         (images, labels, names, id) = ([], [], {}, 1)
#         cams = CameraUser.objects.all()
#         for cam in cams:
#             images.append(cv2.imread(cam.img.url, 0))
#         labels.append(int(1))
#         names[id] = "Binit"
#         (images, labels) = [np.array(lists) for lists in [images, labels]]
#         model = cv2.face.LBPHFaceRecognizer_create()
#         model.train(images, labels)
#         face = None
#         for (x, y, w, h) in faces:
#             face = gray[y:y + h, x:x + w]
#         if (face is not None):
#             face_resize = cv2.resize(face, (width, height))
#             prediction = model.predict(face_resize)
#             if prediction[1] < 74:
#                 label = names[prediction[0]].strip()
#                 confidence = (prediction[1]) if prediction[1] <= 100.0 else 100.0
#                 conf = round((confidence / 74.5) * 100)
#                 return label + " " + str(conf)
#             else:
#                 return "Unknown"
#         else:
#             return ""
#
#     def get_frame(self):
#         success, image = self.video.read()
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
#         label = self.get_prediction(gray, faces_detected)
#         for (x, y, w, h) in faces_detected:
#             cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
#             cv2.putText(image, label, (x + 5, (y + 25) + h), cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
#         # frame_flip = cv2.flip(image,1)
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

import cv2, os, urllib.request
import numpy as np
from django.conf import settings
from .models import Aadhaar_database



face_detection_videocam = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR, 'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_prediction(self, gray, faces, aadhaar_number):
        (width, height) = (130, 100)
        (images, labels, names, id) = ([], [], {}, 1)
        cams = Aadhaar_database.objects.filter(aadhaar_number = aadhaar_number)
        for cam in cams:
            path = settings.BASE_DIR +"\media_cdn"+ cam.image.url
            images.append(cv2.imread(path, 0))
            names[id] = cam.name
            # print(images[0].shape)
        # images.clear()
        # images.append(cv2.imread(
        #     "C:\\Users\\Binit\\Downloads\\Django_VideoStream-master\\Django_VideoStream-master\\streamapp\\7.png", 0))
        #print(images[0].shape)
        labels.append(int(1))
        # names[id] = "Binit"
        (images, labels) = [np.array(lists) for lists in [images, labels]]
        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(images, labels)
        face = None
        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
        if (face is not None):
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            if prediction[1] < 74:
                label = names[prediction[0]].strip()
                confidence = (prediction[1]) if prediction[1] <= 100.0 else 100.0
                conf = round((confidence / 74.5) * 100)
                return label + " " + str(conf)
            else:
                return "Unknown"
        else:
            return ""

    def get_frame(self, aadhaar_number):
        success, image = self.video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        if(faces_detected != ()):
            if(faces_detected.shape[0] > 1):
                label = "Multiple"
            else:
                label = self.get_prediction(gray, faces_detected, aadhaar_number)
                # for (x, y, w, h) in faces_detected:
                #     cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
                #     cv2.putText(image, label, (x + 5, (y + 25) + h), cv2.FONT_HERSHEY_PLAIN, 1.5, (20, 185, 20), 2)
        else:
            label = "No One"
        # frame_flip = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return [jpeg.tobytes(), label]