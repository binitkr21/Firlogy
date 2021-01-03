from django.db import models

# Create your models here.
class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    aadhaar_number = models.CharField(max_length=12)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    password = models.CharField(max_length=15, null=False, blank=False)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    number_of_cases = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)