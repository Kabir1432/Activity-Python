from rest_framework import serializers

from activityngo.custom_auth.serializers import UserPhotoSerializer
from activityngo.fcm.models import PushNotification


class PushNotificationSerializer(serializers.ModelSerializer):
    sender_profile = serializers.SerializerMethodField()

    class Meta:
        model = PushNotification
        fields = ("id", "created", "type", "title", "body", "public", "sender_profile")

    def get_sender_profile(self, obj):
        if not obj.sender:
            return None
        return UserPhotoSerializer(obj.sender).data["image"]
