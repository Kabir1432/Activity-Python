import uuid as uuid
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
from tinymce.models import HTMLField

# from activityngo.college.models import College
from activityngo.custom_auth.managers import ApplicationUserManager
from activityngo.custom_auth.mixins import UserPhotoMixin
from activityngo.utils.sendgrid_email_send import sub_admin_reset_password_mail
# from activityngo.entities.models import State, Degree, Branch, Batches
# from activityngo.university.models import University
from activityngo.utils.utils import (get_walkthrought_random_filename,
                                     set_otp_reset_expiration_time)


# from ..utils.email_send import sub_admin_reset_password_mail

class MultiToken(Token):
    user = models.ForeignKey(  # changed from OneToOne to ForeignKey
        settings.AUTH_USER_MODEL,
        related_name="tokens",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )


# Create your models here.
class BaseModel(models.Model):
    """This model is used for every model in same fields"""

    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ApplicationUser(AbstractBaseUser, UserPhotoMixin, PermissionsMixin):
    GENDER_TYPES = Choices(
        ("male", "Male"),
        ("female", "Female"),
        ("others", "Others"),
    )

    USER_TYPES = Choices(
        ("student", "Student"),
        ("admin", "Admin"),  # admin
        ("sub_admin", "Sub Admin"),  # admin
        ("ngo", "NGO"),
        ("college", "College"),
    )

    # uuid = universal unique identification
    username_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        unique=True,
        help_text=_(
            "Required. A 32 hexadecimal digits number as specified in RFC 4122"
        ),
        error_messages={
            "unique": _("A user with that uuid already exists."),
        },
        default=uuid.uuid4,
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=(
            "Required. 150 characters or fewer. Lettres , digits and @/./+/-/ only ."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _("email address"),
        null=True,
        blank=True,
        unique=True,
        error_messages={"unique": _("A user with that email already exists.")},
    )

    is_email_verified = models.BooleanField(
        _("email verified"),
        default=False,
    )

    first_name = models.CharField(
        _("first name"),
        max_length=30,
        blank=True,
    )

    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )
    fullname = models.CharField(
        _("full name"),
        max_length=300,
        blank=True,
        help_text=_("Full name as it was returned by social provider"),
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether the user should be treated as active."
            "Unselect this instead of deleting account."
        ),
    )

    is_delete = models.BooleanField(
        _("delete"),
        default=False,
        help_text=_("Designates whether this user has been deleted."),
    )

    date_joined = models.DateTimeField(_("Registered date"), default=timezone.now)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True)
    last_user_activity = models.DateTimeField(_("last activity"), default=timezone.now)
    phone = PhoneNumberField(
        _("Mobile Number"),
        null=True,
        blank=True,
        unique=True,
        error_messages={"unique": _("A user with that phone already exists.")},
    )
    gender = models.CharField(
        max_length=10, choices=GENDER_TYPES, null=True, blank=True
    )
    address = models.TextField(_("Address"), null=True, blank=True)
    user_type = models.CharField(
        _("User Type"),
        max_length=16,
        choices=USER_TYPES,
        default=USER_TYPES.admin,
        null=True,
        blank=True,
    )
    device_type = models.CharField(
        _("Device Type"), max_length=1, null=True, blank=True
    )
    device_token = models.CharField(
        _("Device Token"), max_length=256, null=True, blank=True
    )
    device_id = models.CharField(_("Device Id"), max_length=256, null=True, blank=True)
    os_version = models.CharField(_("OS Version"), max_length=8, null=True, blank=True)
    device_name = models.CharField(
        _("Device Name"), max_length=64, null=True, blank=True
    )
    model_name = models.CharField(_("Model Name"), max_length=64, null=True, blank=True)
    ip_address = models.CharField(_("IP Address"), max_length=32, null=True, blank=True)

    # Social Login Fields
    LOGIN_TYPE = (
        ("S", _("Simple")),
        ("A", _("Apple")),
        ("F", _("Facebook")),
        ("G", _("Google")),
    )
    login_type = models.CharField(
        _("Login Type"), choices=LOGIN_TYPE, default="S", max_length=2
    )
    social_key = models.CharField(
        _("Social Key"), max_length=2048, blank=True, null=True
    )

    objects = ApplicationUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # email
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    # def __str__(self):
    #     return self.email or self.first_name or self.last_name or self.str(uuid)

    def save(self, *args, **kwargs):
        if self.photo and (not self.width_photo or not self.height_photo):
            self.width_photo = self.photo.width
            self.height_photo = self.photo.height

        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

        if self.username == "":
            self.username = None
        #     new_username = self.email.split('@')[0] if self.email else ''
        #
        #     if self._meta.model._default_manager.filter(username=new_username).exists() or new_username == '':
        #         postfix = timezone.now().strftime('%Y%m%d%H%M%S')
        #
        #         while self._meta.model._default_manager.filter(username=new_username + postfix).exists():
        #             postfix = timezone.now().strftime('%Y%m%d%H%M%S')
        #
        #         new_username += postfix
        #
        #     self.username = new_username

        if self.fullname:
            self.assign_first_last_name_to_the_object()
        is_new_object = not self.pk  # Check if the object has a primary key
        super(ApplicationUser, self).save(*args, **kwargs)

        user = self
        if is_new_object and (
                user.user_type == "sub_admin" or user.user_type == "college"
        ):
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            reset_link = None
            if user.user_type == "admin" or user.user_type == "sub_admin":
                reset_link = f"{settings.ADMIN_BASE_URL}/auth/reset-password-confirm/{uid}/{token}"
            elif user.user_type == "college":
                reset_link = (
                    f"{settings.COLLEGE_BASE_URL}/reset-password-confirm/{uid}/{token}"
                )
            elif user.user_type == "ngo":
                reset_link = (
                    f"{settings.NGO_BASE_URL}/auth/reset-password-confirm/{uid}/{token}"
                )
            sub_admin_reset_password_mail(user, reset_link)

    def assign_first_last_name_to_the_object(self):
        fullname = self.fullname.split(" ")
        self.first_name = fullname[0]
        if len(fullname) > 1:
            self.last_name = fullname[1]
        else:
            self.last_name = fullname[0]

    def update_last_activity(self):
        now = timezone.now()

        self.last_user_activity = now
        self.save(update_fields=("last_user_activity", "last_modified"))


class Otp(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.IntegerField()
    expiration_time = models.DateTimeField(default=set_otp_reset_expiration_time)


class WalkthroughSlides(BaseModel):
    meta_value = HTMLField()


class Walkthrough(BaseModel):
    title = models.CharField(_("Title"), max_length=256)
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("Walkthrough")
        verbose_name_plural = _("Walkthrough")

    def __str__(self):
        return self.title


class WalkthroughMedia(BaseModel):
    walkthrough = models.ForeignKey(
        Walkthrough, on_delete=models.CASCADE, related_name="walkthrough_media"
    )
    image = models.ImageField(
        upload_to=get_walkthrought_random_filename,
        height_field="height_photo",
        width_field="width_photo",
        null=True,
        blank=True,
    )

    width_photo = models.PositiveSmallIntegerField(blank=True, null=True)
    height_photo = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("Walkthrough Media")
        verbose_name_plural = _("Walkthrough Medias")

    def __str__(self):
        return str(self.walkthrough)

    def save(self, *args, **kwargs):
        if self.image and (not self.width_photo or not self.height_photo):
            self.width_photo = self.photo.width
            self.height_photo = self.photo.height


class UserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(auto_now=True)
