import random

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from templated_email import send_templated_mail
from unicef_restlib.views import MultiSerializerViewSetMixin

from activityngo.custom_auth.models import ApplicationUser
from activityngo.registrations.serializers import (CheckEmailSerializer,
                                                   CheckUserDataSerializer,
                                                   RegistrationSerializer,
                                                   VerificationOtpSerializer)
from activityngo.student.models import StudentOTP
# from activityngo.utils.email_send import verify_otp_sing_up
from activityngo.utils.permissions import IsAPIKEYAuthenticated
from activityngo.utils.sendgrid_email_send import verify_otp_sing_up

class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = ApplicationUser.objects.all()
    serializer_class = RegistrationSerializer
    serializer_action_classes = {
        "check_user_data": CheckUserDataSerializer,
        "send_sms": CheckEmailSerializer,
        "verification_otp": VerificationOtpSerializer,
    }
    permission_classes = (
        AllowAny,
        IsAPIKEYAuthenticated,
    )

    @action(
        methods=["post"],
        permission_classes=(AllowAny, IsAPIKEYAuthenticated),
        url_name="check",
        url_path="check",
        detail=False,
    )
    def check_user_data(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    # @action(methods=['post'], permission_classes=(AllowAny, IsAPIKEYAuthenticated,), url_name='check',
    #         url_path='check', detail=False)
    # def check_user_data(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=self.request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #
    #     # Send SMS code
    #     otp = random.randint(1000, 9999)
    #     email = serializer.validated_data.get("email")
    #     site = get_current_site(request)
    #
    #     # send Email
    #     send_templated_mail(
    #         template_name="reset_password",
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[email],
    #         context={
    #             'domain': site.domain,
    #             'otp': otp,
    #             # 'password_reset_id': password_reset_obj.id,
    #             'protocol': 'http',
    #             'email': email,
    #             'name': 'Registration Otp Verify',
    #         }
    #     )
    #
    #     data = serializer.data
    #     data.update({'otp': otp})
    #     return Response(data)

    @action(
        permission_classes=(
            AllowAny,
            IsAPIKEYAuthenticated,
        ),
        methods=["post"],
        url_name="send_sms_code",
        url_path="send-sms-code",
        detail=False,
    )
    def send_sms(self, request, *args, **kwargs):
        """
        For manual sms code sending
        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        if ApplicationUser.objects.filter(email=email).exists():
            raise ValidationError(_("User already exists with this email."))
        # delete old otp
        StudentOTP.objects.filter(email=email).delete()

        # creating new otp

        otp = random.randint(1000, 9999)
        StudentOTP.objects.create(email=email, otp=otp)

        # site = get_current_site(request)
        verify_otp_sing_up(email, otp)
        # send Email
        # send_templated_mail(
        #     template_name="reset_password",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[email],
        #     context={
        #         'domain': site.domain,
        #         'otp': otp,
        #         # 'password_reset_id': password_reset_obj.id,
        #         'protocol': 'http',
        #         'email': email,
        #         'name': 'Registration Resend Otp Verify',
        #     }
        # )

        data = serializer.data
        data.update({"otp": otp})
        return Response(data)

    @action(
        permission_classes=(
            AllowAny,
            IsAPIKEYAuthenticated,
        ),
        methods=["post"],
        url_name="verification-otp",
        url_path="verification-otp",
        detail=False,
    )
    def verification_otp(self, request, *args, **kwargs):
        """
        For verify otp code sending
        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")

        student_otp = StudentOTP.objects.filter(
            email=email, otp=otp, expiration_time__gt=timezone.now()
        ).first()

        if not student_otp:
            raise ValidationError(_("OTP not verified."))
        student_otp.delete()

        return Response(
            {"details": "OTP verified Successfully !!"}, status=status.HTTP_200_OK
        )
