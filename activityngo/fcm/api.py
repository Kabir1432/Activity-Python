from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from fcm_django.models import FCMDevice
from firebase_admin._messaging_utils import Notification
from firebase_admin.messaging import Message
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from activityngo.fcm.models import PushNotification
from activityngo.fcm.serializers import PushNotificationSerializer
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class CustomFCMDeviceViewSet(FCMDeviceAuthorizedViewSet):
    queryset = FCMDevice.objects.all()
    permissions = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]

    def create(self, request, *args, **kwargs):
        # Delete any existing FCM device for the current user
        FCMDevice.objects.filter(user=request.user).delete()

        # Create a new FCM device
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        FCMDevice.objects.filter(registration_id=kwargs["registration_id"]).update(
            active=False
        )
        try:
            self.request.auth.delete()
        except Exception:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class PushNotificationViewSet(ModelViewSet):
    queryset = PushNotification.objects.all()
    serializer_class = PushNotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(receiver=self.request.user).order_by("-created")
            queryset.update(is_read=True)
        return queryset


class SendNotification:
    REVIEW_TYPE = "Add new Product user"

    @classmethod
    def send_push_notification(cls, user_id, data, title, body):
        # try:
        target_device = FCMDevice.objects.filter(user_id__in=user_id, type="android")
        # print(target_device)
        if target_device:
            target_device.send_message(
                Message(
                    data=data,
                    # notification=Notification(
                    #     title=title,
                    #     body=body
                    # )
                )
            )
        # except Exception as e:
        #     pass

    @classmethod
    def demo_notification(cls, user_id, request_user, product):
        title = "test notification"
        body = f"{request_user} test notification"
        cls.send_push_notification(
            user_id=[user_id],
            data={"push_type": cls.REVIEW_TYPE, "product": str(product)},
            title=title,
            body=body,
        )
        PushNotification.objects.create(
            type=cls.REVIEW_TYPE,
            sender=request_user,
            receiver=user_id,
            title=title,
            body=body,
        )

    @classmethod
    def add_product_notification(cls, request_user, product, data, user_id):
        title = "New Product"

        body = f"{product} is available"
        data["title"] = "New Product"
        data["body"] = f"{product} is available"
        print(data)
        cls.send_push_notification(user_id=user_id, data=data, title=title, body=body)
        # my_obj = []
        # print(user_id)
        my_obj = [
            PushNotification(
                type=cls.REVIEW_TYPE,
                sender=request_user,
                receiver=id,
                title=title,
                body=body,
            )
            for id in user_id
        ]
        # print(my_obj)
        PushNotification.objects.bulk_create(my_obj)[0]

        # FixedAssetsImage.objects.bulk_create(bulk_images)[0]
