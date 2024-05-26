import logging
from datetime import datetime

from activityngo.cron_logger.models import CronLogger
from activityngo.discount.models import Discount


def discount_start_end_cron():
    try:
        current_date = datetime.now().date()

        discounts_to_activate = Discount.objects.filter(active_date=current_date)
        discounts_to_activate.update(is_active=True)

        discounts_to_deactivate = Discount.objects.filter(expire_date=current_date)
        discounts_to_deactivate.update(is_active=False)
        CronLogger.objects.create(
            cron_name="discount_start_end_cron",
            is_error=f"Cron complete successfully. discounts_to_activate:-->{discounts_to_deactivate.count()},discounts_to_activate:-->{discounts_to_activate.count()}",
            is_cron_complete_successfully=True,
        )
    except Exception as e:
        CronLogger.objects.create(
            cron_name="discount_start_end_cron",
            is_error=e,
            is_cron_complete_successfully=False,
        )
