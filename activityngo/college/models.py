from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from activityngo.custom_auth.models import ApplicationUser, BaseModel
from activityngo.entities.models import Batches, Branch, Degree, ProjectCategory, State
from activityngo.ngo.utils import generate_slug_from_uuid
from activityngo.university.models import University

# collage -->CollegeDegree -->branch -->CollegeBatches

# LJ -->1D-->Bechlor --> 1B BCA -->1 2019-2022
#                                 2 2020-2023
#                         2B Bcom
#       2D-->Master


# Create your models here.
class College(BaseModel):
    name = models.CharField(
        _("College Name"),
        max_length=240,
        unique=True,
        error_messages={
            "unique": _("College name already exists."),
        },
    )
    address = models.TextField(_("College Address"))
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="college_state",
    )
    university = models.ManyToManyField(
        University,
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("College")
        verbose_name_plural = _("Colleges")


class CollegeDegree(BaseModel):
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="colleges_degree"
    )
    degree = models.ForeignKey(
        Degree, on_delete=models.CASCADE, related_name="college_degree"
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("College Degree")
        verbose_name_plural = _("College Degree")
        unique_together = ("college", "degree")


class DegreeBranch(BaseModel):
    college_degree = models.ForeignKey(
        CollegeDegree, on_delete=models.CASCADE, related_name="college_degree_branch"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="college_branch",
        null=True,
        blank=True,
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Degree Branch")
        verbose_name_plural = _("Degree Branch")
        unique_together = ("college_degree", "branch")


class BranchBatches(BaseModel):
    degree_branch = models.ForeignKey(
        DegreeBranch, on_delete=models.CASCADE, related_name="college_degree_batches"
    )
    batches = models.ForeignKey(
        Batches, on_delete=models.CASCADE, related_name="college_batches"
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Branch Batches")
        verbose_name_plural = _("Branch Batches")
        unique_together = ("degree_branch", "batches")


class CollegeUsers(BaseModel):
    user = models.OneToOneField(
        ApplicationUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="college_users",
    )
    access_url = models.URLField(_("Access Url"))
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="college_user_state"
    )
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name="college_user_university"
    )
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="professors_college"
    )
    degree = models.ForeignKey(
        CollegeDegree, on_delete=models.CASCADE, related_name="college_user_degree"
    )
    branch = models.ForeignKey(
        DegreeBranch, on_delete=models.CASCADE, related_name="college_user_branch"
    )
    report_link = models.CharField(
        _("Report Link"), max_length=256, null=True, blank=True
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("College Users")
        verbose_name_plural = _("College Users")


class CollegeCollaboration(BaseModel):
    meta_key = models.CharField(max_length=32, unique=True, null=True, blank=True)
    meta_value = HTMLField()
    slug = models.SlugField(_("slug"), max_length=64, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.meta_key)
        super().save(*args, **kwargs)


class CollegeCMS(BaseModel):
    META_KEY = (
        ("about_us", "about_us"),
        ("our_work", "OUR WORK"),
        ("activity_point_projects", "Activity Point Projects"),
        ("contact_us", "Contact Us"),
    )
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="college_cms"
    )
    meta_key = models.CharField(max_length=32, choices=META_KEY)
    slug = models.SlugField(
        _("slug"), max_length=64, unique=True, null=True, blank=True
    )
    meta_value = HTMLField()

    class Meta:
        verbose_name = _("College CMS")
        verbose_name_plural = _("College CMS")
        unique_together = ("college", "meta_key")

    def save(self, *args, **kwargs):
        self.slug = slugify(generate_slug_from_uuid())
        super().save(*args, **kwargs)
