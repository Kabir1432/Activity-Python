from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from model_utils import Choices

from activityngo.custom_auth.models import BaseModel

User = get_user_model()


class PushNotification(BaseModel):
    TYPES = Choices(
        ("admin_notification", "Admin Notification"),
        ("testing_notification", "Testing Notification"),
    )

    type = models.CharField(
        _("Notification Type"), null=True, blank=True, max_length=128
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender", null=True, blank=True
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver", null=True, blank=True
    )
    title = models.CharField(_("Title"), null=True, blank=True, max_length=128)
    body = models.TextField(
        _("Body"),
        null=True,
        blank=True,
    )
    public = models.BooleanField(
        _("Public"),
        default=False,
    )
    is_read = models.BooleanField(
        _("Read"),
        default=False,
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _("Notifications")
