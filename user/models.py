from django.db import models

# Create your models here.

class User(models.Model):
    aadhaar_number =models.CharField(max_length=12, primary_key=True)
    email = models.EmailField()
    password= models.CharField(max_length=30)
    phone_number= models.CharField(max_length=10, unique=True,null=True)

class Aadhaar_database(models.Model):
    aadhaar_number =models.CharField(max_length=12, primary_key=True)
    name= models.CharField(max_length=100)
    image=models.ImageField(upload_to='media')
    phone_number =models.CharField(max_length= 10, unique=True)
    state = models.CharField(max_length=30, blank= True, null= True)
    city = models.CharField(max_length=30, blank= True, null= True)
    address=models.CharField(max_length=200)
    gender = models.CharField(max_length= 10, null = True, blank= True)
    dob = models.DateField(null = True, blank= True)
    signature = models.FileField(upload_to='signature', blank=True ,null=True)
    audio = models.FileField(upload_to='audio', blank=True ,null=True)

class Fir(models.Model):
    case_id=models.AutoField(primary_key= True)
    fir_id= models.CharField(max_length=10,blank=True ,null=True)
    aadhaar_number=models.CharField(max_length=12)
    fir_for=models.CharField(max_length=10)
    o_relation = models.CharField(max_length= 30, blank=True,null=True)
    o_victim = models.CharField(max_length= 100, blank=True,null=True)
    o_gender= models.CharField(max_length=10, blank=True,null=True)
    fatherorhusbandName = models.CharField(max_length= 100, blank=True,null=True)
    city=models.CharField(max_length=30)
    police_station=models.CharField(max_length=100)
    date=models.CharField(max_length=20)
    time= models.CharField(max_length=10)
    complaint= models.TextField()
    accused_description= models.TextField(blank=True)
    suspected_criminal= models.CharField(max_length=30, blank=True,null=True)
    evi =models.CharField(max_length=1000,blank=True,null=True)
    status = models.CharField(max_length=50)
    io = models.CharField(max_length=20 , blank=True ,null=True)
    volunteer =models.CharField(max_length=12,blank=True,null=True)
    facilitator=models.CharField(max_length=12,blank=True ,null=True)
    compainant_signature=models.ImageField(upload_to='signature',blank=True ,null=True)
    sho_signature=models.ImageField(upload_to='signature', blank=True ,null=True)
    sho_reject = models.FileField(upload_to='audio', blank=True ,null=True) 
    sp_reject = models.FileField(upload_to='audio', blank=True ,null=True)
    iochargesheet=models.FileField(upload_to='chargesheet', blank=True ,null=True)
    ioevidence= models.CharField(max_length=1000,blank=True,null=True)
    affidavit = models.FileField(upload_to='affidavit', blank=True ,null=True)
    paadhaar = models.CharField(max_length=12, blank= True, null= True)
    curdate = models.CharField(max_length= 20, blank= True, null = True)
    # edate = models.CharField(max_length= 20, blank= True, null= True)


class Evidence(models.Model):
    evidence_id=models.AutoField(primary_key=True)
    case_id= models.CharField(max_length=20)
    evidence_type=models.CharField(max_length=20)
    evidence_file=models.FileField(upload_to='evidence')

class Storage(models.Model):
     aadhaar_number =models.CharField(max_length=12, primary_key=True)
     file1 = models.FileField(upload_to='evidence', blank=True,null=True)
     file2 = models.ImageField(upload_to='signature')


class Store(models.Model):
    aadhaar_number = models.CharField(max_length=12)
    file1 = models.FileField(upload_to='evidence', blank=True, null=True)

class Signature(models.Model):
    aadhaar_number = models.CharField(max_length=12)
    file1 = models.FileField(upload_to='evidence', blank=True, null=True)


class OTPValidator(models.Model):
    otp = models.CharField(max_length=10)
    aadhaar_number = models.CharField(max_length=12, primary_key= True)

class GETVolunteer(models.Model):
    request_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length= 50)
    phone_number = models.CharField(max_length= 10)
    email = models.EmailField()
    state = models.CharField(max_length= 50)
    city = models.CharField(max_length= 50)
    address = models.CharField(max_length= 200)
    status = models.CharField(max_length= 30, blank= True, null= True)
    vid = models.CharField(max_length= 12, blank= True, null= True)


class FaceRecog(models.Model):
    aadhaar_number = models.CharField(max_length= 12)
    known = models.IntegerField()
    unknown = models.IntegerField()
    noone = models.IntegerField(blank= True, null= True)

class UserNotification(models.Model):
    case_id = models.IntegerField(primary_key= True)
    aadhaar_number = models.CharField(max_length= 12)
    user_read = models.IntegerField()
    status = models.CharField(max_length=50)
    date = models.DateField()

class UserNotify(models.Model):
    case_id = models.IntegerField(primary_key= True)
    aadhaar_number = models.CharField(max_length= 12)
    user_read = models.IntegerField()
    status = models.CharField(max_length=50)
    date = models.DateField()

class BlockEvidence(models.Model):
    case_id = models.CharField(max_length= 12)
    date = models.CharField(max_length= 30, blank= True, null= True)
    transaction = models.CharField(max_length= 1000)

class BlockTable(models.Model):
    block_id = models.AutoField(primary_key = True)
    case_id = models.CharField(max_length= 12)
    block = models.CharField(max_length= 200)




