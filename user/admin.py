from django.contrib import admin
from .models import User, OTPValidator
from .models import Aadhaar_database
from .models import Fir , Evidence ,Storage,Store, GETVolunteer, FaceRecog, UserNotify, BlockEvidence, BlockTable
# Register your models here.

admin.site.register(User)
admin.site.register(Aadhaar_database)
admin.site.register(Fir)
admin.site.register(Evidence)
admin.site.register(Storage)
admin.site.register(OTPValidator)
admin.site.register(Store)
admin.site.register(GETVolunteer)
admin.site.register(FaceRecog)
admin.site.register(UserNotify)
admin.site.register(BlockEvidence)
admin.site.register(BlockTable)
