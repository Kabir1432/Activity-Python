from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from rest_framework.exceptions import ValidationError
from tinymce.models import HTMLField

from activityngo.college.models import College, CollegeDegree, DegreeBranch, BranchBatches
from activityngo.custom_auth.models import ApplicationUser, BaseModel
from activityngo.entities.models import Batches, Branch, Degree, State
from activityngo.student.utils import (generate_complaint_number,
                                       generate_student_membership_id_code,
                                       set_otp_expiration_time)
from activityngo.sub_admin.models import SubAdmin
from activityngo.university.models import University
from activityngo.utils.utils import (get_complaint_photo_random_filename,
                                     get_llp_Certificate_path,
                                     get_student_complaint_path)


class StudentDetails(BaseModel):
    # For student collage student use from collage ForeignKey
    student = models.OneToOneField(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="student_details",
        verbose_name=_("Student"),
    )
    student_state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="student_states",
        verbose_name=_("Student State"),
    )
    college_state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="college_states",
        verbose_name=_("Student College State"),
    )
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="student_university",
        verbose_name=_("Student University"),
    )
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name="student_college",
        verbose_name=_("Student College"),
    )
    degree = models.ForeignKey(
        CollegeDegree,
        on_delete=models.CASCADE,
        related_name="student_degree",
        verbose_name=_("Student Degree"),
    )
    branch = models.ForeignKey(
        DegreeBranch,
        on_delete=models.CASCADE,
        related_name="student_branch",
        verbose_name=_("Student Branch"),
    )
    batch = models.ForeignKey(
        BranchBatches,
        on_delete=models.CASCADE,
        related_name="student_batch",
        verbose_name=_("Student Batch"),
    )
    id_number = models.CharField(_("Student ID Number"), max_length=64)  # this is number is given by college
    student_membership_id = models.CharField(
        _("Student Membership id"), max_length=30, unique=True, null=True, blank=True
    )
    deactivation_date = models.DateTimeField(_("deactivation date"), null=True)
    student_ip_address = models.CharField(
        _("Student IP Address"), max_length=50, null=True, blank=True
    )
    google_full_name = models.CharField(_('Google full name'), max_length=128, null=True)
    disable_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new_object = not self.pk  # Check if the object has a primary key
        if is_new_object:
            try:
                number = generate_student_membership_id_code()
                if not number:
                    raise ValidationError("Reach limit of entry.")
                self.student_membership_id = number
            except:
                raise ValidationError("Reach limit of entry.")
        return super(StudentDetails, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        student = self.student
        super(StudentDetails, self).delete(*args, **kwargs)
        student.delete()


# class ContactUS(BaseModel):
#     """
#     Define ContactUS Model to use ContactUS Details Store
#     """
#
#     firstName = models.CharField(_("firstName"), max_length=64)
#     lastName = models.CharField(_("lastName"), max_length=64)
#     email = models.CharField(_("Email"), max_length=128)
#     subject = models.CharField(_("Subject"), max_length=128)
#     description = models.TextField(_("Description"))
#
#     class Meta:
#         verbose_name = _("ContactUS")
#         verbose_name_plural = _("ContactUS")
#
#     def __str__(self):
#         return f"{self.email}"


class AboutUs(BaseModel):
    meta_value = HTMLField()


class TermsAndCondition(BaseModel):
    meta_value = HTMLField()


class OurTeam(BaseModel):
    meta_value = HTMLField()


class Necessity(BaseModel):
    meta_value = HTMLField()


class AicteRules(BaseModel):
    meta_value = HTMLField()


class Implementation(BaseModel):
    meta_value = HTMLField()


class Complaints(BaseModel):
    PRIORITY = Choices(
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    )

    STATUS = Choices(
        ("open", "Open"),
        ("processing", "Processing"),
        ("closed", "Closed"),
    )

    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="student_complaints",
        null=True,
        blank=True,
    )
    issue = models.TextField(_("Issue"), null=True, blank=True)
    complaint_number = models.CharField(
        _("Complaint number"), max_length=15, null=True, blank=True
    )
    priority = models.CharField(
        _("Priority"), max_length=16, choices=PRIORITY, null=True, blank=True
    )
    allotted_to = models.ForeignKey(
        SubAdmin,
        on_delete=models.CASCADE,
        related_name="allotted_to",
        null=True,
        blank=True,
    )
    status = models.CharField(
        _("Status"), choices=STATUS, default="open", max_length=16
    )
    resolution_provided = models.CharField(
        _("Resolution Provided"), max_length=512, null=True
    )
    upload_file = models.FileField(
        _("upload_file"), upload_to=get_student_complaint_path, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Complaint")
        verbose_name_plural = _("Complaints")

    # def __str__(self):
    #     return f"{self.student}"

    def save(self, *args, **kwargs):
        is_new_object = not self.pk  # Check if the object has a complaint number
        if is_new_object:
            try:
                number = generate_complaint_number()
                if not number:
                    raise ValidationError("Reach limit of entry.")
                self.complaint_number = number
            except:
                raise ValidationError("Reach limit of entry.")
        return super(Complaints, self).save(*args, **kwargs)


class ComplaintsMedia(BaseModel):
    complaints = models.ForeignKey(
        Complaints, on_delete=models.CASCADE, related_name="complaints_media"
    )
    photo = models.ImageField(
        upload_to=get_complaint_photo_random_filename,
        height_field="height_photo",
        width_field="width_photo",
    )

    width_photo = models.PositiveSmallIntegerField(blank=True, null=True)
    height_photo = models.PositiveSmallIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.photo and (not self.width_photo or not self.height_photo):
            self.width_photo = self.photo.width
            self.height_photo = self.photo.height


class StudentOTP(BaseModel):
    email = models.EmailField(_("email"))
    otp = models.PositiveIntegerField(_("OTP"), null=True, blank=True)
    expiration_time = models.DateTimeField(default=set_otp_expiration_time)
    is_verified = models.BooleanField(default=0)

    def save(self, *args, **kwargs):
        self.expiration_time = set_otp_expiration_time()
        return super().save()
