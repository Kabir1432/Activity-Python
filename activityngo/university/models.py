from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from activityngo.custom_auth.models import BaseModel
from activityngo.entities.models import ProjectCategory, State
from activityngo.ngo.utils import generate_slug_from_uuid


# Create your models here.
class University(BaseModel):
    name = models.CharField(
        _("University Name"),
        max_length=64,
        unique=True,
        error_messages={
            "unique": _("University name already exists."),
        },
    )
    address = models.TextField(_("University Address"))
    state = models.ManyToManyField(State)
    project_category = models.ManyToManyField(ProjectCategory)
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("University")
        verbose_name_plural = _("Universities")

    def __str__(self):
        return self.name


class UniversityRules(BaseModel):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="university_rules",
        verbose_name=_("University Rules"),
    )
    meta_value = HTMLField()


class UniversityCollaboration(BaseModel):
    meta_key = models.CharField(max_length=32, unique=True, null=True, blank=True)
    meta_value = HTMLField()
    slug = models.SlugField(_("slug"), max_length=64, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.meta_key)
        super().save(*args, **kwargs)


class UniversityCMS(BaseModel):
    META_KEY = (
        ("about_us", "about_us"),
        ("our_work", "OUR WORK"),
        ("activity_point_projects", "Activity Point Projects"),
        ("contact_us", "Contact Us"),
    )
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name="university_cms"
    )
    meta_key = models.CharField(max_length=32, choices=META_KEY)
    slug = models.SlugField(
        _("slug"), max_length=64, unique=True, null=True, blank=True
    )
    meta_value = HTMLField()

    class Meta:
        verbose_name = _("University CMS")
        verbose_name_plural = _("University CMS")
        unique_together = ("university", "meta_key")

    def save(self, *args, **kwargs):
        self.slug = slugify(generate_slug_from_uuid())
        super().save(*args, **kwargs)
