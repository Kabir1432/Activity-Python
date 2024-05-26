import phonenumbers
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from activityngo.custom_auth.models import ApplicationUser


class CheckEmailSerializer(Serializer):
    email = serializers.EmailField(required=True)


class VerificationOtpSerializer(Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.IntegerField(required=True)


class CheckOtp(Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=4, required=True)


class CheckUserDataSerializer(ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = ("email", "fullname", "social_key", "login_type")
        extra_kwargs = {
            "email": {"required": True},
            "fullname": {"required": True},
            "social_key": {"required": True},
            "login_type": {"required": True},
        }


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = (
            "fullname",
            "email",
            "phone",
            "password",
            "uuid",
            "gender",
        )
        extra_kwargs = {
            "password": {"write_only": True, "validators": [validate_password]},
            "email": {"required": True},
            "fullname": {"required": True},
            "gender": {"required": True},
        }
        read_only_fields = ("uuid",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)

        # password assigment
        user.set_password(password)
        user.save(update_fields=["password"])

        return user
