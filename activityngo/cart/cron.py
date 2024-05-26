from activityngo.cart.models import Cart
from activityngo.cron_logger.models import CronLogger


def empty_cart_model():
    try:
        cart_delete = Cart.objects.all().delete()
        CronLogger.objects.create(
            cron_name="empty_cart_model",
            is_error=f"Cron complete successfully,cart_delete :--{cart_delete}",
            is_cron_complete_successfully=True,
        )
    except Exception as e:
        CronLogger.objects.create(
            cron_name="empty_cart_model",
            is_error=e,
            is_cron_complete_successfully=False,
        )
