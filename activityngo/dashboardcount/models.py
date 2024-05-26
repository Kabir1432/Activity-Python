from django.db import models

from activityngo.custom_auth.models import BaseModel


# Create your models here.
# class Download
class AppDownload(models.Model):
    download_count = models.PositiveIntegerField(default=0)
