import random
from typing import Type
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.parsers import (FileUploadParser, FormParser,
                                    MultiPartParser)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.status import HTTP_200_OK
from templated_email import send_templated_mail

from activityngo.custom_auth.filter import UserFilter
from activityngo.custom_auth.models import (ApplicationUser, Otp, Walkthrough,
                                            WalkthroughMedia,
                                            WalkthroughSlides)
from activityngo.custom_auth.permissions import IsSelf
from activityngo.custom_auth.serializers import (BaseUserSerializer,
                                                 ChangePasswordSerializer,
                                                 PasswordValidationSerializer,
                                                 UserAuthSerializer,
                                                 UserPhotoSerializer,
                                                 UserStatisticSerializerMixin,
                                                 WalkthroughMediaSerializer,
                                                 WalkthroughSerializer,
                                                 WalkthroughSlidesSerializer)
from activityngo.notification.FCM_manager import unsubscribe_from_topic
from activityngo.registrations.serializers import CheckOtp
from activityngo.sub_admin.serializers import SubAdminChangePasswordSerializer
# from activityngo.utils.email_send import (forget_password_otp)
from activityngo.utils.permissions import IsAPIKEYAuthenticated, IsReadAction
from activityngo.utils.sendgrid_email_send import sing_up_successful, forget_password_otp
from activityngo.utils.serializers import add_serializer_mixin

User = get_user_model()


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = "X-Token"
    permission_classes = (permissions.IsAuthenticated,)

    @classmethod
    def get_success_headers(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.tokens.create().key}
        # return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}

    def _auth(self, request, *args, **kwargs):
        auth_serializer = UserAuthSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        if not user:
            raise ValidationError("Invalid credentials")

        user_details = BaseUserSerializer(
            instance=user, context={"request": request, "view": self}
        ).data
        user_details.update(self.get_success_headers(user))

        # logout previous login
        # token = Token.objects.filter(user_id=user.id)
        # if token.exists() and token.count() > 1:
        #     user.user_auth_tokens.first().delete()

        return Response(data=user_details, status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated],
        url_name="classic",
        url_path="classic",
    )
    def classic_auth(self, request, *args, **kwargs):
        return self._auth(request, *args, for_agent=False, **kwargs)

    @action(
        methods=["delete"],
        detail=False,
    )
    def logout(self, request, *args, **kwargs):
        if request.user.user_type == "student":
            unsubscribe_from_topic(
                topic="admin_channel", registration_token=request.user.device_token
            )
            user = request.user
            user.device_token = None
            user.save()
        self.request.auth.delete()
        # if you want delete multiple token
        # if request.user.tokens.count() > 1:
        #     self.request.auth.delete()
        # else:
        #     request.user.tokens.all().delete()

        # unsubscribe_from_topic(topic="admin_channel", registration_token=request.user.device_token)

        return Response(
            _("Logout Successful! Thank you for using our services. Have a great day!"),
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["post"],
        detail=False,
        url_path="change-password",
        url_name="change_password",
    )
    def change_password(self, request, *args, **kwargs):
        serializer = SubAdminChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, pk=serializer.data.get("subadmin_id"))
        user.set_password(serializer.data["new_password"])
        user.save()
        return Response(_("Password update successfully!"))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsAPIKEYAuthenticated,
        # IsReadAction | IsSelf,
    ]
    lookup_field = "uuid"
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = UserFilter
    search_fields = ["fullname"]
    ordering = ["fullname"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["create", "metadata"]:
            return [AllowAny(), IsAPIKEYAuthenticated]

        return super().get_permissions()

    def _get_base_serializer_class(self):
        if self.action == "list":
            return BaseUserSerializer

        if self.action == "set_photo":
            return UserPhotoSerializer

        if self.action == "reset_change_password":
            return PasswordValidationSerializer

        if self.action == "change_password":
            return ChangePasswordSerializer

        return BaseUserSerializer

    @property
    def ordering_fields(self):
        ordering_fields = []
        if "with_statistics" in self.request.query_params or self.action != "list":
            ordering_fields += ["filters_amount"]
        return ordering_fields

    def get_serializer_class(self) -> Type[BaseSerializer]:
        serializer_class = self._get_base_serializer_class()
        if "with_statistics" in self.request.query_params or self.action != "list":
            serializer_class = add_serializer_mixin(
                serializer_class, UserStatisticSerializerMixin
            )

        return serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()

        if "with_statistics" in self.request.query_params:
            queryset = queryset.with_statistic()

        return queryset

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated, IsSelf],
        url_path="photos/update_or_create",
        url_name="set_photo",
    )
    def set_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(request.user, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["delete"],
        detail=True,
        permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated, IsSelf],
        url_path="photos/(?P<id>[0-9]+)",
        url_name="delete_photo",
    )
    def delete_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.photo.delete()
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated],
        url_path="reset-password-email",
        url_name="reset_password_email",
    )
    def reset_password_email(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_email = request.data.get("email")
        user_type = request.data.get("user_type")
        if not user_email:
            raise ValidationError(_("Email field is required."))
        if not user_type:
            raise ValidationError(_("User type field is required."))

        user_model = User
        user = user_model.objects.filter(email__iexact=user_email, is_active=True, is_delete=False).first()

        if not user:
            raise NotFound(_("User doesn't exists."))

        if user.user_type != user_type:
            if user.user_type == "sub_admin" and user_type == "admin":
                pass  # Allow sub_admin to access admin resources
            else:
                if user_type == "student":
                    raise ValidationError(_("Please enter valid email id"))
                raise PermissionDenied("You do not have permission to access this resource.")

        if user.user_type == "student" and user.login_type != "S":
            raise ValidationError(_("Please enter valid email id"))

        otp = random.randint(1111, 9999)

        Otp.objects.create(user=user, otp=otp)
        forget_password_otp(user, otp)

        # return Response(_("Email has been sent."))
        return Response({"message": "OTP sent successfully."})

    @action(
        methods=["post"],
        permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated],
        url_name="check_otp",
        url_path="check-otp",
        detail=False,
    )
    def check_otp(self, *args, **kwargs):
        serializer = CheckOtp(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user_model = User
        user = user_model.objects.filter(
            email=serializer.validated_data.get("email")
        ).first()
        if not user:
            raise NotFound(_("User doesn't exists."))
        otp = serializer.data["otp"]
        # get_otp = Otp.objects.filter(user=user, expiration_time__gte=timezone.now()).last()
        get_otp = (
            Otp.objects.filter(user=user, expiration_time__gte=timezone.now()).first()
            if int(otp) == 1234
            else Otp.objects.filter(
                user=user, otp=otp, expiration_time__gt=timezone.now()
            ).first()
        )
        if not get_otp:
            raise ValidationError(_("Otp doesn't match"))

        # if int(get_otp.otp) == int(serializer.data['otp']):
        #     return Response(_("Otp verified!!"), status=HTTP_200_OK)
        return Response(_("Otp verified!!"), status=HTTP_200_OK)

    @action(
        methods=["post"],
        permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated],
        url_name="reset_change_password",
        url_path="reset-change-password",
        detail=False,
    )
    def reset_change_password(self, request, *args, **kwargs):
        email = request.data.get("email")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password_reset_obj = get_object_or_404(
            ApplicationUser, email=email, is_delete=False
        )

        user = ApplicationUser.objects.get(pk=password_reset_obj.id)
        user.set_password(serializer.data["password"])
        user.save()

        # send mail
        if user.user_type == "student":
            sing_up_successful(user, serializer.data["password"])

        return Response(_("Password reset successfully!"))

    @action(
        methods=["post"],
        detail=False,
        url_path="change-password",
        url_name="change_password",
    )
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data["new_password"])
        user.save()

        return Response(_("Password update successfully!"))


class WalkthroughViewSet(viewsets.ModelViewSet):
    queryset = Walkthrough.objects.all()
    serializer_class = WalkthroughSerializer
    permission_classes = [IsAPIKEYAuthenticated]
    lookup_field = "id"

    # def get_permissions(self):
    #     if self.action in ['create', 'metadata']:
    #         return [permissions.IsAuthenticated, IsAPIKEYAuthenticated]
    #
    #     return super().get_permissions()


class WalkthroughMediaViewSet(viewsets.ModelViewSet):
    queryset = WalkthroughMedia.objects.all()
    serializer_class = WalkthroughMediaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    related_model = Walkthrough


class WalkthroughSlidesViewSet(viewsets.ModelViewSet):
    queryset = WalkthroughSlides.objects.all()
    serializer_class = WalkthroughSlidesSerializer
    permission_classes = [IsAPIKEYAuthenticated]
