from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


class PushNotification:
    @classmethod
    def _send_push_notification(cls, user_id, data, title, body):
        target_device = FCMDevice.objects.filter(user_id__in=user_id, type="android")

        target_device.send_message(
            Message(data=data, notification=Notification(title=title, body=body))
        )

    @classmethod
    def send_notification_to_all_students(cls, notification):
        cls._send_push_notification(
            user_id=[notification.receiver.id],
            data={
                "receiver": str(notification.receiver.id),
                "sender": str(notification.sender.id),
                "tag": str(notification.tag),
                "title": str(notification.title),
                "message": str(notification.message),
                "model_id": str(notification.model_id),
            },
            title=str(notification.title),
            body=str(notification.message),
        )

    def send_notification_to_all_student(cls, notification, obj):
        cls._send_push_notification(
            user_id=notification,
            data={
                "receiver": str(notification),
                "sender": str(obj.sender),
                "tag": str(obj.tag),
                "title": str(obj.title),
                "message": str(obj.message),
                "model_id": str(obj.model_id),
            },
            title=str(notification.title),
            body=str(notification.message),
        )

    @classmethod
    def send_notification_to_group_of_students(cls, notification):
        cls._send_push_notification(
            user_id=[notification.receiver.id],
            data={
                "receiver": str(notification.receiver.id),
                "sender": str(notification.sender.id),
                "tag": str(notification.tag),
                "title": str(notification.title),
                "message": str(notification.message),
                "model_id": str(notification.model_id),
            },
            title=str(notification.title),
            body=str(notification.message),
        )

    @classmethod
    def send_notification_to_individual_student(cls, notification):
        cls._send_push_notification(
            user_id=[notification.receiver.id],
            data={
                "receiver": str(notification.receiver.id),
                "sender": str(notification.sender.id),
                "tag": str(notification.tag),
                "title": str(notification.title),
                "message": str(notification.message),
                "model_id": str(notification.model_id),
            },
            title=str(notification.title),
            body=str(notification.message),
        )

    @classmethod
    def send_admin_notification(cls, notification, obj):
        cls._send_push_notification(
            user_id=notification,
            data={
                "receiver": str(notification),
                "tag": str("admin"),
                "title": str(obj.title),
                "message": str(obj.message),
            },
            title=str(obj.title),
            body=str(obj.message),
        )
