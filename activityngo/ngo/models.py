from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from tinymce.models import HTMLField

from activityngo.custom_auth.models import ApplicationUser, BaseModel
from activityngo.entities.models import State
from activityngo.ngo.utils import (generate_franchise_code,
                                   generate_slug_from_uuid)
from activityngo.university.models import University
from activityngo.utils.utils import (get_cancelled_cheque_path,
                                     get_dpiit_document_path,
                                     get_franchise_certificate_path,
                                     get_gstin_document_path,
                                     get_llp_Certificate_path, get_logo_path,
                                     get_ngo_office_photo_path,
                                     get_pan_card_path,
                                     get_seal_and_sign_of_director_1_path,
                                     get_seal_and_sign_of_director_2_path,
                                     get_seal_and_sign_of_trustee_3_path,
                                     get_tan_card_path, get_trust_deed,
                                     get_trustee_1_Aadhar_card_path,
                                     get_trustee_2_aadhar_card_path,
                                     get_udhyam_aadhar_document_path)


class Ngo(BaseModel):
    ngo_name = models.CharField(_("Ngo name"), max_length=35, unique=True)
    franchise_code = models.CharField(
        _("Franchise code"), max_length=30, unique=True, null=True, blank=True
    )
    state = models.ManyToManyField(State, blank=True)
    university = models.ManyToManyField(University, blank=True)
    disable_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new_object = not self.pk  # Check if the object has a primary key
        if is_new_object:
            try:
                number = generate_franchise_code()
                if not number:
                    raise ValidationError("Reach limit of entry.")
                self.franchise_code = number
            except:
                raise ValidationError("Reach limit of entry.")
        return super(Ngo, self).save(*args, **kwargs)


class Franchise(BaseModel):
    user = models.OneToOneField(
        ApplicationUser,
        on_delete=models.CASCADE,
        null=True,
        related_name="user_franchise",
    )
    ngo = models.OneToOneField(
        Ngo, on_delete=models.CASCADE, null=True, related_name="ngo_franchise"
    )
    entity_name = models.CharField(_("Entity Name"), max_length=50)
    entity_name_in_report = models.CharField(_("Entity Name in Report"), max_length=40)
    address = models.CharField(_("Address"), max_length=150)
    geo_tag = models.CharField(_("GEO Tag"), max_length=64)
    gstin = models.CharField(
        _("GSTIN"),
        max_length=64,
    )
    pan_no = models.CharField(
        _("PAN No"),
        max_length=64,
    )
    tan_no = models.CharField(
        _("TAN No"),
        max_length=64,
        null=True
        , blank=True
    )
    ngo_commission_percentage = models.FloatField(
        _("NGO Commission in Percentage"), max_length=20
    )

    def delete(self, *args, **kwargs):
        user = self.user
        super(Franchise, self).delete(*args, **kwargs)
        user.delete()


class Organization(BaseModel):
    user = models.OneToOneField(
        ApplicationUser,
        on_delete=models.CASCADE,
        null=True,  # store id for admin
        related_name="user_organization",
    )  # in case of admin profile admin id will store either it will be null
    franchise = models.OneToOneField(
        Franchise,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="franchise_organization",
    )  # in case of NGO profile franchise id will store either it will be null
    organization_name = models.CharField(
        _("Organization Name"), null=True, max_length=50
    )
    type = models.CharField(
        _("Organization Type"),
        max_length=64,
    )
    address = models.TextField(
        _("Address"),
    )
    geo_tag = models.CharField(
        _("Geo Tag"),
        max_length=64,
    )
    organization_location_state = models.CharField(
        _("Organization Location State"),
        null=True,
        max_length=64,
    )
    email = models.EmailField(
        _("Email"),
        null=True,
        unique=True,
        error_messages={"unique": _("A user with that email already exists.")},
    )
    contact_no = PhoneNumberField(
        _("Mobile Number"),
        null=True,
        unique=True,
        error_messages={"unique": _("A user with that phone already exists.")},
    )
    latitude = models.DecimalField(
        _("latitude"),
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(-90)],
    )
    longitude = models.DecimalField(
        _("longitude"),
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(-180)],
    )
    # point = models.PointField(srid=4326)
    pan_no = models.CharField(
        _("PAN No"),
        max_length=64,
    )
    tan_no = models.CharField(
        _("TAN No"),
        max_length=64,
        null=True,
        blank=True
    )
    gstin = models.CharField(
        _("GSTIN"),
        max_length=64,
    )
    udhyam_aadhar_certificate_number = models.CharField(
        _("Udhyam Aadhar Certificate Number"),
        max_length=64,
    )
    dpiit_certificate_number = models.CharField(
        _("DPIIT Certificate Number"),
        max_length=64,
    )
    llpin = models.CharField(
        _("LLPIN"),
        max_length=64,
    )
    website = models.URLField(_("Website"), null=True,
                              blank=True)
    no_of_directors = models.CharField(
        _("No. of Directors"), max_length=64, null=True, blank=True
    )
    project_name = models.CharField(
        _("Project Name"),
        max_length=64,
    )

    ngo_darpan_no = models.CharField(_("Organization Type"), null=True, blank=True, max_length=64, )
    cinno = models.CharField(_("Organization Type"), null=True,
                             blank=True, max_length=64, )
    username = models.CharField(_('Username'), unique=True, max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    # def __str__(self):
    #     return self.email


class Directors(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="organization_directors"
    )
    trustee_name = models.CharField(
        _("Trustee Name"),
        max_length=64,
    )
    designation = models.CharField(
        _("Designation"),
        max_length=64,
    )
    director_no = models.CharField(
        _("Director No"), max_length=64, null=True, blank=True
    )
    pan_no = models.CharField(_("PAN No"), max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = _("Director")
        verbose_name_plural = _("Directors")

    def __str__(self):
        return self.trustee_name


class Bank(BaseModel):
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name="organization_bank"
    )
    account_name = models.CharField(
        _("Account Name"),
        max_length=64,
    )
    account_number = models.CharField(
        _("Account Number"),
        max_length=64,
    )
    account_type = models.CharField(
        _("Account Type"),
        max_length=64,
    )
    ifsc_code = models.CharField(
        _("IFSC Code"),
        max_length=64,
    )
    bank_name = models.CharField(
        _("Bank Name"),
        max_length=64,
    )
    bank_branch = models.CharField(
        _("Bank Branch"),
        max_length=64,
    )
    upi_number = models.CharField(
        _("UPI Number"),
        max_length=64,
    )
    mobile = PhoneNumberField(
        _("Mobile Number"),
        unique=True,
        error_messages={"unique": _("A user with that phone already exists.")},
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": _("A user with that email already exists.")},
    )

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")

    def __str__(self):
        return self.account_name


class OrganizationAttachments(BaseModel):
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name="organization_attachments"
    )
    tagline = models.CharField(_("Tagline"), max_length=64, null=True, blank=True)
    llp_Certificate = models.FileField(
        _("LLP Certificate"), upload_to=get_llp_Certificate_path, null=True, blank=True
    )
    gstin_document = models.FileField(
        _("GSTIN Document"), upload_to=get_gstin_document_path, null=True, blank=True
    )
    udhyam_aadhar_document = models.FileField(
        _("Udhyam Aadhar Document"),
        upload_to=get_udhyam_aadhar_document_path,
        null=True,
        blank=True,
    )
    dpiit_document = models.FileField(
        _("DPIIT Document"), upload_to=get_dpiit_document_path, null=True, blank=True
    )
    pan_card = models.FileField(
        _("PAN Card"), upload_to=get_pan_card_path, null=True, blank=True
    )
    tan_card = models.FileField(
        _("TAN Card"), upload_to=get_tan_card_path, null=True, blank=True
    )
    logo = models.FileField(_("Logo"), upload_to=get_logo_path, null=True, blank=True)
    trustee_1_Aadhar_card = models.FileField(
        _("Trustee - 1 Aadhar Card"),
        upload_to=get_trustee_1_Aadhar_card_path,
        null=True,
        blank=True,
    )
    trustee_2_aadhar_card = models.FileField(
        _("Trustee - 2 Aadhar Card"),
        upload_to=get_trustee_2_aadhar_card_path,
        null=True,
        blank=True,
    )
    cancelled_cheque = models.FileField(
        _("Cancelled Cheque"),
        upload_to=get_cancelled_cheque_path,
        null=True,
        blank=True,
    )
    seal_and_sign_of_director_1 = models.FileField(
        _("Seal and Sign of Director 1"),
        upload_to=get_seal_and_sign_of_director_1_path,
        null=True,
        blank=True,
    )
    seal_and_sign_of_director_2 = models.FileField(
        _("Seal and Sign of Director 2"),
        upload_to=get_seal_and_sign_of_director_2_path,
        null=True,
        blank=True,
    )

    ngo_office_photo = models.FileField(
        _("NGO Office Photo"),
        upload_to=get_ngo_office_photo_path,
        null=True,
        blank=True,
    )
    seal_and_sign_of_trustee_3 = models.FileField(
        _("Seal and Sign of Trustee 3"),
        upload_to=get_seal_and_sign_of_trustee_3_path,
        null=True,
        blank=True,
    )
    franchise_certificate = models.FileField(
        _("Franchise Certificate"),
        upload_to=get_franchise_certificate_path,
        null=True,
        blank=True,
    )
    trust_deed = models.FileField(
        _("Trust Deed / Sec 8 Document"),
        upload_to=get_trust_deed,
        null=True,
        blank=True,
    )


class NGOCollaboration(BaseModel):
    meta_key = models.CharField(max_length=32, unique=True, null=True, blank=True)
    meta_value = HTMLField()
    slug = models.SlugField(_("slug"), max_length=64, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.meta_key)
        super().save(*args, **kwargs)


class NgoCMS(BaseModel):
    META_KEY = (
        ("about_us", "about_us"),
        ("our_work", "OUR WORK"),
        ("activity_point_projects", "Activity Point Projects"),
        ("contact_us", "Contact Us"),
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="organization_cms"
    )
    meta_key = models.CharField(max_length=32, choices=META_KEY)
    slug = models.SlugField(
        _("slug"), max_length=64, unique=True, null=True, blank=True
    )
    meta_value = HTMLField()

    class Meta:
        verbose_name = _("Ngo CMS")
        verbose_name_plural = _("Ngo CMS")
        unique_together = ("organization", "meta_key")

    def save(self, *args, **kwargs):
        self.slug = slugify(generate_slug_from_uuid())
        super().save(*args, **kwargs)
