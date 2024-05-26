from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

from activityngo.custom_auth.models import BaseModel

# Create your models here.


class CronLogger(BaseModel):
    cron_type = Choices(
        ("discount_start_end_cron", "discount_start_end_cron"),
        ("remove_log_of_after_7_days", "remove_log_of_after_7_days"),
        ("empty_cart_model", "empty_cart_model"),
        ("inactive_student_after_1_year", "inactive_student_after_1_year"),
        ("inactive_5_year_old_student", "inactive_5_year_old_student"),
        ("order_expire", "order_expire"),
        ("soft_delete_notification", "soft_delete_notification"),
    )
    cron_name = models.CharField(_("Cron Name"), choices=cron_type, max_length=100)
    is_error = models.CharField(_("Is Error"), max_length=1000)
    is_cron_complete_successfully = models.BooleanField(
        _("Is cron complete successfully")
    )


class ServerErrorHandel(BaseModel):
    error_name = models.CharField(_("Error Name"), max_length=32)
    error = models.TextField(_("Error"))
    request_data = models.TextField(_("Request Data"), null=True, blank=True)
    request_path = models.TextField(_("Request Path"), null=True, blank=True)
    request_api = models.TextField(_("Request API"), null=True, blank=True)
