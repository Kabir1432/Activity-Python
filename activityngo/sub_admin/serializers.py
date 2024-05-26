from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activityngo.custom_auth.models import ApplicationUser
from activityngo.sub_admin.models import (CustomPermission, SubAdmin,
                                          UserAccessPermission,
                                          UserAdminAccessLog)


class UserPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(source="photo", allow_null=True)
    width = serializers.ReadOnlyField(source="width_photo", allow_null=True)
    height = serializers.ReadOnlyField(source="height_photo", allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "image", "width", "height")


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    photo = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationUser
        fields = (
            "id",
            "username",
            "email",
            "fullname",
            "phone",
            "gender",
            "address",
            "user_type",
            "date_joined",
            "first_name",
            "last_name",
            "photo",
            "password",
        )
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "fullname": {"required": True},
            "phone": {"required": True},
            "gender": {"required": True},
            "address": {"required": True},
            "date_joined": {"required": True},
            "password": {"required": False},
            "user_type": {"required": True},
        }
        read_only_fields = ("first_name", "last_name")

    def get_photo(self, obj):
        photo = obj.photo
        if not photo:
            return
        return UserPhotoSerializer(obj).data

    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)

        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user


class SubAdminSerializer(serializers.ModelSerializer):
    # user_details = UserSerializer(required=True, write_only=True, many=False, partial=True)
    user_detail = UserSerializer(source="user", read_only=True)
    user_details = serializers.JSONField(write_only=True)

    class Meta:
        model = SubAdmin
        fields = [
            "id",
            "user",
            "date_of_birth",
            "alternate_mobile",
            "alternate_email",
            "employee_number",
            "designation",
            "pan_no",
            "aadhar_no",
            "blood_group",
            "disable_date",
            "user_detail",
            "user_details",
            "is_active",
        ]
        extra_kwargs = {
            "date_of_birth": {"required": True},
            "alternate_mobile": {"required": True},
            "alternate_email": {"required": True},
            "employee_number": {"required": True},
            "designation": {"required": True},
            "pan_no": {"required": True},
            "aadhar_no": {"required": True},
            "blood_group": {"required": True},
        }
        read_only_fields = ["user"]

    @transaction.atomic
    def create(self, validated_data):
        parent_data = validated_data.pop("user_details")
        parent_serializer = UserSerializer(data=parent_data)
        parent_serializer.is_valid(raise_exception=True)
        parent = parent_serializer.save()
        validated_data["user"] = parent
        data = super().create(validated_data)
        permissions = CustomPermission.objects.all()
        user_permissions = [UserAccessPermission(user=data.user, custom_permission=permission) for permission in
                            permissions]
        UserAccessPermission.objects.bulk_create(user_permissions)
        return data

    def update(self, instance, validated_data):
        """Delete can be done only after the 90 days of DISABLE"""

        instance = super().update(instance, validated_data)
        if instance.is_active is False:
            current_time = timezone.now()
            instance.disable_date = current_time
            instance.save()
        elif instance.is_active is True:
            instance.disable_date = None
            instance.save()

        # update user data
        if "user_details" in validated_data:
            parent_data = validated_data.pop("user_details")
            parent_serializer = UserSerializer(
                instance.user, data=parent_data, partial=True
            )
            parent_serializer.is_valid(raise_exception=True)
            parent_serializer.save()

        return instance

    def get_fields(self):
        fields = super().get_fields()

        # Check if the context contains the update operation
        view = self.context.get("view")
        if view and hasattr(view, "action"):
            if (
                    self.context["view"].action == "update"
                    or self.context["view"].action == "partial_update"
            ):
                # Add field names to be read-only during update
                readonly_fields = ["disable_date"]
                for field_name in readonly_fields:
                    if field_name in fields:
                        fields[field_name].read_only = True
        return fields


class PasswordResetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()


class CustomPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = ("id", "name")


class UserAccessPermissionSerializer(serializers.ModelSerializer):
    custom_permission_data = serializers.SerializerMethodField()

    class Meta:
        model = UserAccessPermission
        fields = (
            "id",
            "user",
            "custom_permission",
            "custom_permission_data",
            "is_read_access",
            "is_update_access",
        )
        extra_kwargs = {
            "user": {"required": True},
            "custom_permission": {"required": True},
            "is_read_access": {"required": True},
            "is_update_access": {"required": True},
        }

    def get_custom_permission_data(self, obj):
        return obj.custom_permission.name

    # @transaction.atomic
    # def create(self, validated_data):
    #     user = self.context.get('user') or self.context.get('request').user
    #     validated_data['user'] = user
    #     return super().create(validated_data)


class SubAdminAccessLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = UserAdminAccessLog
        fields = ("id", "create_time", "user", "action", "model_name", "user_name")

    def get_user_name(self, obj):
        try:
            return obj.user.fullname
        except:
            return ""


class SubAdminAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    user_type = serializers.CharField(required=False)
    # phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if "username" not in validated_data:
            if "email" not in validated_data:
                raise ValidationError(_("Email should be provided"))

        return validated_data


class SubAdminChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    subadmin_id = serializers.CharField(required=True)


class UserAccessPermissionBulkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccessPermission
        fields = (
            "id",
            "user",
            "custom_permission",
            "is_read_access",
            "is_update_access",
        )
