from django.utils import timezone

from activityngo.cron_logger.models import CronLogger
from activityngo.order.models import OrderDetail


def set_order_expire():
    try:
        current_date = timezone.now()
        order_expire = OrderDetail.objects.filter(expire_on__lte=current_date).update(
            is_expire=True
        )

        CronLogger.objects.create(
            cron_name="order_expire",
            is_error=f"Cron complete successfully order expire:-->{order_expire}",
            is_cron_complete_successfully=True,
        )
    except Exception as e:
        CronLogger.objects.create(
            cron_name="order_expire", is_error=e, is_cron_complete_successfully=False
        )
