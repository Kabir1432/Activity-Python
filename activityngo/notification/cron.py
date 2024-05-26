from django.utils import timezone

from activityngo.cron_logger.models import CronLogger
from activityngo.notification.models import Notification


def set_order_expire():
    try:
        latest_50_ids = (
            Notification.objects.all().order_by("-create_time").values("id")[:50]
        )
        updated_count = Notification.objects.exclude(id__in=latest_50_ids).update(
            is_active=False
        )

        CronLogger.objects.create(
            cron_name="soft_delete_notification",
            is_error=f"Cron complete successfully soft delete:-->{updated_count}",
            is_cron_complete_successfully=True,
        )
    except Exception as e:
        CronLogger.objects.create(
            cron_name="order_expire", is_error=e, is_cron_complete_successfully=False
        )
