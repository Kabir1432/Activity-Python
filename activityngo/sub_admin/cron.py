from datetime import datetime, timedelta

from activityngo.cron_logger.models import CronLogger
from activityngo.sub_admin.models import UserAdminAccessLog


def remove_log_of_after_7_days():
    try:
        seven_days_ago = datetime.now() - timedelta(days=1)

        # Delete data older than 7 days
        deleted_count = UserAdminAccessLog.objects.filter(
            create_time__lt=seven_days_ago
        ).delete()
        CronLogger.objects.create(
            cron_name="remove_log_of_after_7_days",
            is_error=f"Cron complete successfully deleted_count:-->{deleted_count}",
            is_cron_complete_successfully=True,
        )
    except Exception as e:
        CronLogger.objects.create(
            cron_name="remove_log_of_after_7_days",
            is_error=e,
            is_cron_complete_successfully=False,
        )
