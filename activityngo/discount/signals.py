from django.db.models.signals import post_save
from django.dispatch import receiver

from activityngo.discount.models import Discount, DiscountUsage


@receiver(post_save, sender=Discount)
def update_order_status(sender, instance, created, **kwargs):
    if not created and not instance.discount_limit_reached:
        if instance.current_discount_usage_count == instance.usage_limit:
            instance.discount_limit_reached = True
            instance.save()
        # obj = instance
        # obj.discount.current_discount_usage_count += 1
        # obj.save()
