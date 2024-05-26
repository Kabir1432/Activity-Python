from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from activityngo.custom_auth.models import ApplicationUser, BaseModel


class SubAdmin(BaseModel):
    user = models.OneToOneField(
        ApplicationUser,
        on_delete=models.CASCADE,
        null=True,
        related_name="user_subAdmin",
    )
    date_of_birth = models.DateField(_("Date of birth"), null=True, blank=True)
    alternate_mobile = PhoneNumberField(
        _("Alternate Mobile Number"),
        null=True,
        blank=True,
    )
    alternate_email = models.EmailField(
        _("Alternate Email Address"),
        null=True,
        blank=True,
    )
    employee_number = models.CharField(
        _("Employee Number"), max_length=64, null=True, blank=True
    )
    designation = models.CharField(
        _("Designation"), max_length=50, null=True, blank=True
    )
    pan_no = models.CharField(_("PAN No"), max_length=32, null=True, blank=True)
    aadhar_no = models.CharField(_("Aadhar No"), max_length=50, null=True, blank=True)
    blood_group = models.CharField(
        _("Blood Group"), max_length=50, null=True, blank=True
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Sub Admin")
        verbose_name_plural = _("Sub Admins")

    def delete(self, *args, **kwargs):
        user = self.user
        super(SubAdmin, self).delete(*args, **kwargs)
        user.delete()


class CustomPermission(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserAccessPermission(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    custom_permission = models.ForeignKey(CustomPermission, on_delete=models.CASCADE)
    is_read_access = models.BooleanField(_("Read Access"), default=False)
    is_update_access = models.BooleanField(_("Update Access"), default=False)

    def __str__(self):
        return f"{self.user.username} - {self.custom_permission.name}"

    class Meta:
        verbose_name = _("User Access Permission")
        verbose_name_plural = _("User Access Permission")
        unique_together = (
            "user",
            "custom_permission",
        )


class UserAdminAccessLog(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(_("Action"), max_length=255)
    model_name = models.CharField(_("Module name"), max_length=255)

    def __str__(self):
        return f"{self.user} - {self.action}"
