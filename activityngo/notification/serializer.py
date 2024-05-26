from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from activityngo.notification.models import Notification


class PushNotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        exclude = ["is_active", "is_delete", "update_time"]


class SendNotificationSerializer(ModelSerializer):
    user = serializers.IntegerField(required=False)
    project = serializers.IntegerField(required=False)

    class Meta:
        model = Notification
        fields = ["tag", "message", "user", "project"]
        extra_kwargs = {
            "tag": {"required": True},
            "message": {"required": True},
        }

    def validate(self, attrs):
        if attrs.get("tag") == "group_of_students":
            if "project" not in attrs:
                raise ValidationError(_("project field is required"))

        elif attrs.get("tag") == "individual_student":
            if "user" not in attrs:
                raise ValidationError(_("user field is required"))

        return super().validate(attrs)


class PromotionalEmailSerializer(serializers.Serializer):
    to_email = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=50), required=True
    )
    subject = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
