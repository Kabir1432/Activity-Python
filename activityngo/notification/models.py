from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

from activityngo.custom_auth.models import BaseModel
from activityngo.student.models import StudentDetails


# Create your models here.
class Notification(BaseModel):
    TYPES = Choices(
        ("all_students", "All Students"),
        ("group_of_students", "Group of Students"),
        ("individual_student", "Individual Student"),
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_receiver",
        null=True,
        blank=True,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_sender",
        null=True,
        blank=True,
    )
    tag = models.CharField(
        _("Notification Tag"), max_length=32, null=True, blank=True, choices=TYPES
    )
    title = models.CharField(
        _("Notification Title"), max_length=64, null=True, blank=True
    )
    message = models.CharField(
        _("Notification Message"), max_length=512, null=True, blank=True
    )
    model_id = models.IntegerField(_("Model Id"), null=True, blank=True)
    is_public = models.BooleanField(_("Is Public"), default=False)
    is_read = models.BooleanField(default=False)
    group_of_student = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="group_of_student_notification"
    )

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
