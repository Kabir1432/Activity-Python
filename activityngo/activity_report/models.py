from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from tinymce.models import HTMLField

from activityngo.custom_auth.models import BaseModel
from activityngo.project.models import Project


# Create your models here.
class ReportContent(BaseModel):
    POINT = Choices(
        ("points_20", "POINT_20"),
        ("points_10", "POINT_10"),
        ("points_05", "POINT_05"),
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_report_content"
    )
    type_point = models.CharField(
        _("type point"),
        max_length=40,
        choices=POINT,
    )

    disclaimer = HTMLField(null=True)
    abstract = HTMLField(null=True)
    chapter_01 = HTMLField(null=True)
    chapter_02 = HTMLField(null=True)
    chapter_03 = HTMLField(null=True)
    chapter_04 = HTMLField(null=True)
    chapter_05 = HTMLField(null=True)
    chapter_06 = HTMLField(null=True)
    chapter_07 = HTMLField(null=True)
    appendix = HTMLField(null=True)
    disable_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Report Content")
        verbose_name_plural = _("Report Content")
        unique_together = ("project", "type_point")
