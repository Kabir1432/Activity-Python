from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activityngo.custom_auth.models import ApplicationUser
from activityngo.custom_auth.serializers import UserPhotoSerializer
from activityngo.sub_admin.models import (CustomPermission, SubAdmin,
                                          UserAccessPermission,
                                          UserAdminAccessLog)
from activityngo.sub_admin.renderer import SubAdminRenderer
from activityngo.sub_admin.serializers import (
    CustomPermissionSerializer, ResetPasswordSerializer,
    SubAdminAccessLogSerializer, SubAdminAuthSerializer,
    SubAdminChangePasswordSerializer, SubAdminSerializer,
    UserAccessPermissionBulkUpdateSerializer, UserAccessPermissionSerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated

from .serializers import PasswordResetSerializer
from ..utils.sendgrid_email_send import sub_admin_reset_password_mail


class SubAdminViewSet(viewsets.ModelViewSet):
    queryset = SubAdmin.objects.all()
    serializer_class = SubAdminSerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    renderer_classes = [SubAdminRenderer]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    ordering_fields = ["user__username", "user__first_name", "user__last_name", "user__email"]

    def destroy(self, request, *args, **kwargs):
        """Delete can be done only after the 90 days of DISABLE"""
        instance = self.get_object()
        current_date = timezone.now().date()
        if instance.disable_date:
            remaining_days = (current_date - instance.disable_date.date()).days
            if remaining_days >= 90:
                self.perform_destroy(instance)
            else:
                raise ValidationError(
                    _(f"PENDING DAYS: {90 - remaining_days} to delete the user")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-create_time")

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsAPIKEYAuthenticated],
        url_path="photos/update_or_create",
        url_name="set_photo",
    )
    def set_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        # serializer = UserPhotoSerializer(request.user, data=request.data)
        get_user = ApplicationUser.objects.filter(id=user.user.id).first()
        if not get_user:
            raise ValidationError(_("User not found"))
        serializer = UserPhotoSerializer(get_user, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["delete"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsAPIKEYAuthenticated],
        url_path="photos",
        url_name="delete_photo",
    )
    def delete_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        # user.photo = 'user_photos/default.png'
        user.user.photo.delete()
        # user.photo.delete(save=False)
        # user.photo = ''
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomPermissionViewSet(viewsets.ModelViewSet):
    queryset = CustomPermission.objects.all()
    serializer_class = CustomPermissionSerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ["name", ]

    # search_fields = ['user__username', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-create_time")


class UserAccessPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserAccessPermission.objects.all()
    serializer_class = UserAccessPermissionSerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["id", "user", "custom_permission", "custom_permission__name"]
    ordering_fields = ["custom_permission__name", "user__fullname"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("create_time")

    def partial_update(self, request, *args, **kwargs):
        # Get the list of objects to update from the request data
        data = request.data
        try:
            objects_to_update = []
            for item in data:
                obj_id = item.get("id")
                if obj_id is None:
                    return Response(
                        {"message": "Missing 'id' field for one or more objects"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Fetch the object
                obj = self.get_object()

                # Serialize the data and update the object
                serializer = self.get_serializer(obj, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                objects_to_update.append(obj)

            # You can return a response with updated objects if needed
            serialized_objects = self.get_serializer(objects_to_update, many=True)
            return Response(serialized_objects.data, status=status.HTTP_200_OK)

        except UserAccessPermission.DoesNotExist:
            return Response(
                {"message": "One or more objects not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserAccessPermissionBulkUpdate(APIView):
    def post(self, request, format=None):
        data = request.data
        objects_to_update = []

        for item in data:
            obj_id = item.get("id")
            if obj_id is not None:
                try:
                    obj = UserAccessPermission.objects.get(pk=obj_id)
                    serializer = UserAccessPermissionBulkUpdateSerializer(
                        instance=obj, data=item, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                        objects_to_update.append(serializer.data)
                    else:
                        return Response(
                            serializer.errors, status=status.HTTP_400_BAD_REQUEST
                        )
                except UserAccessPermission.DoesNotExist:
                    return Response(
                        {"message": f"Object with ID {obj_id} not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

        return Response(objects_to_update, status=status.HTTP_200_OK)


class SubAdminAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserAdminAccessLog.objects.all()
    serializer_class = SubAdminAccessLogSerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["user"]
    ordering_fields = ["action", "user__fullname", "model_name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-create_time")


from django.conf import settings


@api_view(["POST"])
@permission_classes([IsAPIKEYAuthenticated])
def send_reset_email(request):
    serializer = PasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # if serializer.is_valid():
    user_id = serializer.validated_data.get("user_id")
    user = get_object_or_404(ApplicationUser, pk=user_id)
    # user = user.user
    # Generate a reset token and send it via email
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    reset_link = None
    if user.user_type == "admin" or user.user_type == "sub_admin":
        reset_link = (
            f"{settings.ADMIN_BASE_URL}/auth/reset-password-confirm/{uid}/{token}"
        )
    elif user.user_type == "college":
        reset_link = f"{settings.COLLEGE_BASE_URL}/reset-password-confirm/{uid}/{token}"
    elif user.user_type == "ngo":
        reset_link = (
            f"{settings.NGO_BASE_URL}/auth/reset-password-confirm/{uid}/{token}"
        )
    sub_admin_reset_password_mail(user, reset_link)

    return JsonResponse({"message": "Password reset link sent successfully."})
    # return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAPIKEYAuthenticated])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        uidb64 = serializer.validated_data.get("uidb64")
        token = serializer.validated_data.get("token")
        new_password = serializer.validated_data.get("new_password")

        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(ApplicationUser, pk=uid)
        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            # Set the new password
            user.set_password(new_password)
            user.save()
            return JsonResponse({"message": "Password reset successfully."})
        else:
            return JsonResponse(
                {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )

    except ApplicationUser.DoesNotExist:
        return JsonResponse(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

    except (TypeError, ValueError, OverflowError):
        raise ValidationError(_("Invalid user or token"))
    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SubAdminAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = "X-Token"
    permission_classes = (permissions.IsAuthenticated,)

    @classmethod
    def get_success_headers(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.tokens.create().key}
        # return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}

    def _auth(self, request, *args, **kwargs):
        auth_serializer = SubAdminAuthSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        if not user and user.user_type != "sub_admin":
            raise ValidationError("Invalid credentials")

        user_details = SubAdminSerializer(
            instance=user.user_subAdmin, context={"request": request, "view": self}
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
        url_name="log-in",
        url_path="log-in",
    )
    def classic_auth(self, request, *args, **kwargs):
        return self._auth(request, *args, for_agent=False, **kwargs)

    @action(methods=["delete"], detail=False)
    def logout(self, request, *args, **kwargs):
        self.request.auth.delete()
        # if you want delete all token
        # if request.user.tokens.count() > 1:
        #     self.request.auth.delete()
        # else:
        #     request.user.tokens.all().delete()
        # request.user.tokens.all().delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post"],
        detail=False,
        url_path="change-password",
        url_name="change_password",
    )
    def change_password(self, request, *args, **kwargs):
        serializer = SubAdminChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(SubAdmin, pk=serializer.data.get("subadmin_id"))
        user = user.user
        user.set_password(serializer.data["new_password"])
        user.save()
        return Response(_("Password update successfully!"))
