from django.db import models

# Create your models here.
class Cctv(models.Model):
    aadhaar_number = models.CharField(max_length=12)
    file =models.FileField(upload_to='cctv')

class Sketch(models.Model):
    sid = models.CharField(max_length= 12)
    sfile = models.FileField(upload_to= 'sketch')
