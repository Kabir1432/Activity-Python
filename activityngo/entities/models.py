from django.db import models
from django.utils.translation import gettext_lazy as _

from activityngo.custom_auth.models import BaseModel


# Create your models here.
class State(BaseModel):
    name = models.CharField(
        _("State Name"),
        max_length=64,
        unique=True,
        error_messages={
            "unique": _("State name already exists."),
        },
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name


class Degree(BaseModel):
    name = models.CharField(
        _("Degree Name"),
        max_length=64,
        unique=True,
        error_messages={
            "unique": _("Degree name already exists."),
        },
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Degree")
        verbose_name_plural = _("Degrees")

    def __str__(self):
        return self.name


class Branch(BaseModel):
    name = models.CharField(
        _("Branch Name"),
        max_length=128,
        unique=True,
        error_messages={
            "unique": _("Branch name already exists."),
        },
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return self.name


class Batches(BaseModel):
    start_year = models.IntegerField(_('Start Year'), null=True)
    end_year = models.IntegerField(_('End Year'), null=True)
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Batch")
        verbose_name_plural = _("Batches")
        # unique_together = ("start_year", "end_year")

    # def __str__(self):
    #     return self.year


class ImplementationBatches(BaseModel):
    start_year = models.IntegerField(_('Start Year'), )
    end_year = models.IntegerField(_('End Year'), )
    disable_date = models.DateTimeField(_('disable date'), null=True, blank=True)

    class Meta:
        verbose_name = _("ImplementationBatches")
        verbose_name_plural = _("ImplementationBatches")
        unique_together = ("start_year", "end_year")


class ProjectCategory(BaseModel):
    name = models.CharField(
        _("Project Category Name"),
        max_length=240,
        unique=True,
        error_messages={
            "unique": _("Activity Category name already exists."),
        },
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Project Category")
        verbose_name_plural = _("Project Categories")

    # def __str__(self):
    #     return self.name


class ProjectType(BaseModel):
    type = models.CharField(
        _("Project Type"),
        max_length=64,
        unique=True,
        error_messages={
            "unique": _("Activity Type already exists."),
        },
    )
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _("Project Types")

    def __str__(self):
        return self.type
