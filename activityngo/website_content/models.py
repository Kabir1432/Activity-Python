from django.db import models
from activityngo.custom_auth.models import BaseModel
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from tinymce.models import HTMLField

from activityngo.utils.utils import get_website_cover_photo_path


# Create your models here.
class WebsiteContent(BaseModel):
    DOMAIN_CHOICE = Choices(
        ("activity_points_engg", "Activity Points engg"),
        ("lgs_research_foundation", "Lgs Research Foundation"),
    )
    PAGES_CHOICE = Choices(
        ("what", "What"),
        ("where", "Where"),
        ("how", "How"),
        ("list", "List"),
        ("who", "Who"),
    )
    domain = models.CharField(_('Domain'), choices=DOMAIN_CHOICE, max_length=40)
    page_name = models.CharField(_('Page'), choices=PAGES_CHOICE, max_length=40)
    meta_value = HTMLField()

    class Meta:
        verbose_name = _("Website Content")
        verbose_name_plural = _("Website Contents")
        unique_together = ("domain", "page_name")


class WebsiteCoverPhoto(BaseModel):
    DOMAIN_CHOICE = Choices(
        ("activity_points_engg", "Activity Points engg"),
        ("lgs_research_foundation", "Lgs Research Foundation"),
    )
    cover_photo = models.ImageField(_("Cover photo"), upload_to=get_website_cover_photo_path)
    domain = models.CharField(_('Domain'), choices=DOMAIN_CHOICE, max_length=40)
