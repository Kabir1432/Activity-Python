from django.contrib import admin

from activityngo.student.models import StudentDetails, StudentOTP

# Register your models here.
admin.site.register(StudentDetails)
admin.site.register(StudentOTP)
