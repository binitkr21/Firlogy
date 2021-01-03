from django.db import models

# Create your models here.

class Police(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=45)
    aadhaar_number = models.CharField(max_length=12)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    police_station = models.CharField(max_length=50)
    password = models.CharField(max_length=15, null=False, blank=False)
    phone_number = models.CharField(max_length=10, null= True, blank= True)
    number_of_cases = models.IntegerField(null= True, blank= True)
    experience = models.IntegerField(null= True, blank= True)
    email = models.EmailField(null=True, blank=True)

class Criminal(models.Model):
    aadhaar_number = models.CharField(max_length=12, null= True, blank= True)
    name = models.CharField(max_length=100)
    crime_type= models.CharField(max_length=50)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    police_station = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    image= models.ImageField(upload_to='criminals', null= True, blank= True)


