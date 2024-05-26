from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activityngo.college.models import CollegeUsers
from activityngo.custom_auth.models import (ApplicationUser, Walkthrough,
                                            WalkthroughMedia,
                                            WalkthroughSlides)
from activityngo.ngo.models import Franchise, Organization

User = get_user_model()


class UserAuthSerializer(serializers.Serializer):
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


class UserPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(source="photo", allow_null=True)
    width = serializers.ReadOnlyField(source="width_photo", allow_null=True)
    height = serializers.ReadOnlyField(source="height_photo", allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "image", "width", "height")


class PasswordValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as ex:
            raise ValidationError(ex.messages)
        return password


class BaseUserSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    ngo = serializers.SerializerMethodField()
    college = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "uuid",
            "fullname",
            "email",
            "user_type",
            "phone",
            "photo",
            "address",
            "gender",
            "password",
            "ngo",
            "college",
            "organization",
            "is_active",
        )
        read_only_fields = ("uuid",)

    def get_photo(self, obj):
        photo = obj.photo
        if not photo:
            return
        return UserPhotoSerializer(obj).data

    def get_ngo(self, obj):
        ngo = Franchise.objects.filter(user=obj).first()
        if ngo:
            return ngo.id
        return None

    def get_organization(self, obj):
        organization = Organization.objects.filter(user=obj).first()
        if organization:
            return organization.id
        return None

    def get_college(self, obj):
        college = CollegeUsers.objects.filter(user=obj).first()
        if college:
            return college.id
        return None

    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)

        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user


class UserStatisticSerializerMixin:
    filters_amount = serializers.ReadOnlyField()

    class Meta:
        fields = ("filters_amount",)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data["old_password"] == validated_data["new_password"]:
            raise ValidationError(
                _(
                    "Aww don't use the same password! For security reasons, please use a different "
                    "password to your old one"
                )
            )
        elif not self.context["request"].user.check_password(
            validated_data["old_password"]
        ):
            raise ValidationError(
                _("You've entered an incorrect old password, please try again.")
            )

        return validated_data


class WalkthroughMediaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    width = serializers.ReadOnlyField(source="width_photo", allow_null=True)
    height = serializers.ReadOnlyField(source="height_photo", allow_null=True)

    class Meta:
        model = WalkthroughMedia
        fields = ["id", "image", "width", "height"]
        extra_kwargs = {"image": {"required": True}}

    def create(self, validated_data):
        images = dict(self.context["request"].data)["image"]
        if len(images) and images[0] == "":
            raise ValidationError(_("Images filed is required."))
        user = Walkthrough.objects.filter(
            id=self.context["view"].kwargs.get("nested_1_id")
        ).first()
        if not user:
            raise ValidationError(_("User not found"))
        bulk_images = [
            WalkthroughMedia(walkthrough=user, image=images[i])
            for i in range(len(images))
        ]
        return WalkthroughMedia.objects.bulk_create(bulk_images)[0]


class WalkthroughSerializer(serializers.ModelSerializer):
    walkthrough_media = WalkthroughMediaSerializer(read_only=True, many=True)

    class Meta:
        model = Walkthrough
        fields = ["id", "title", "description", "walkthrough_media"]


class WalkthroughSlidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkthroughSlides
        fields = ("id", "meta_value")
        read_only = ("id",)
