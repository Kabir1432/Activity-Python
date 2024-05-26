from django.db.models.signals import post_save
from django.dispatch import receiver

from activityngo.notification.FCM_manager import send_to_topic, sendPush
from activityngo.notification.models import Notification


@receiver(post_save, sender=Notification)
def push_notification(sender, instance, created=False, **kwargs):
    """
    Define push_notification signal to use of
    Send Push Notification to User When add new
    notification
    """

    if created:
        """
        When add new notification
        """
        device_token = [str(instance.receiver.device_token)]
        data = {
            "notification_id": str(instance.id),
            "tag": str(instance.tag),
            "model_id": str(instance.model_id),
            "title": str(instance.title),
            "body": str(instance.message),
        }
        title = instance.title
        msg = instance.message

        if instance.is_public:
            send_to_topic(title, msg, "admin_channel", data)
        else:
            sendPush(title, msg, device_token, data)
