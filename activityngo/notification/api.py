import json
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from unicef_restlib.views import MultiSerializerViewSetMixin

from activityngo.custom_auth.models import ApplicationUser
from activityngo.notification.models import Notification
from activityngo.notification.serializer import (
    PromotionalEmailSerializer,
    PushNotificationSerializer,
    SendNotificationSerializer,
)
from activityngo.notification.tasks import (
    send_notification_to_individual_student,
    send_notification_to_group_of_students,
    send_notification_to_all_students,
)
from activityngo.order.models import OrderDetail
from activityngo.utils.permissions import IsAPIKEYAuthenticated, IsReadAction
from activityngo.utils.sendgrid_email_send import (
    send_promotional_email,
)


class PushNotificationViewSet(
    MultiSerializerViewSetMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Notification.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]
    serializer_class = PushNotificationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = [
        "create_time",
        "tag",
        "message",
    ]

    def get_queryset(self):
        if (
            self.request.user.user_type == "admin"
            or self.request.user.user_type == "sub_admin"
        ):
            if self.action == "destroy":
                return super().get_queryset()
            return (
                super(PushNotificationViewSet, self)
                .get_queryset()
                .all()
                # .order_by("-create_time")[:50]
            )
        else:
            queryset = (
                super(PushNotificationViewSet, self)
                .get_queryset()
                .filter(
                    Q(receiver=self.request.user)
                    | Q(group_of_student__in=[self.request.user])
                )
                .order_by("-create_time")
            )

            queryset.update(is_read=True)

            return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post"],
        url_name="push-notification",
        url_path="push-notification",
        detail=False,
        serializer_class=SendNotificationSerializer,
    )
    def send_push_students(self, request, *args, **kwargs):
        # user = self.get_object()
        # self.check_object_permissions(request, user)
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        admin = request.user
        # fcm - send notification to all students
        if serializer.validated_data.get("tag") == "all_students":
            active_subscription_students = OrderDetail.objects.filter(
                is_expire=False, order__is_temp_order=False, order__user__is_active=True
            ).values_list("order__user", flat=True)
            if active_subscription_students:
                unique_users = list(dict.fromkeys(active_subscription_students))
                send_notification_to_all_students.delay(
                    admin.id, request.data, unique_users
                )

        # fcm - send notification to group students
        elif serializer.validated_data.get("tag") == "group_of_students":
            group_of_students = OrderDetail.objects.filter(
                project_id=serializer.validated_data.get("project"),
                is_expire=False,
                order__is_temp_order=False,
                order__user__is_active=True,
            ).values_list("order__user", flat=True)

            if group_of_students:
                unique_users = list(dict.fromkeys(group_of_students))
                send_notification_to_group_of_students.delay(
                    admin.id, request.data, unique_users
                )

        # fcm - send notification to individual students
        elif serializer.validated_data.get("tag") == "individual_student":
            student = ApplicationUser.objects.filter(
                id=serializer.validated_data.get("user"),
                is_active=True,
                is_delete=False,
            ).first()

            if student:
                send_notification_to_individual_student.delay(
                    student.id, admin.id, request.data
                )

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    @action(
        methods=["post"],
        url_name="promotional-emails",
        url_path="promotional-emails",
        detail=False,
        serializer_class=PromotionalEmailSerializer,
    )
    def promotional_emails(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        # send email
        send_promotional_email(
            serializer.validated_data.get("to_email"),
            serializer.validated_data.get("subject"),
            serializer.validated_data.get("body"),
        )

        return Response("Email sent successfully", status=status.HTTP_201_CREATED)
