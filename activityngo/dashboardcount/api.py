from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from activityngo.custom_auth.models import ApplicationUser, UserActivity
from activityngo.dashboardcount.models import AppDownload
from activityngo.dashboardcount.serializer import AppDownloadSerializer
from activityngo.order.models import Order, OrderDetail
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class DashboardCountView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsAPIKEYAuthenticated,
    ]

    def get(self, request, *args, **kargs):
        total_android_application_downloads = (
            AppDownload.objects.all().first().download_count
            if AppDownload.objects.all().first()
            else 0
        )
        total_student_memberships = ApplicationUser.objects.filter(
            user_type="student"
        ).count()
        total_project_subscriptions = OrderDetail.objects.filter(order__is_temp_order=False).count()
        # subscription_expired_without_project_completion = OrderDetail.objects.filter(expire_date__gte=timezone.now()).count()
        subscription_expired_without_project_completion = OrderDetail.objects.filter(
            is_expire=True, order__is_temp_order=False, is_complete=False

        ).count()
        total_reports_generated = OrderDetail.objects.filter(
            order__is_temp_order=False, activity_status="complete"

        ).count()

        # Calculate a time threshold for considering a user as online (e.g., last 5 minutes)
        online_threshold = timezone.now() - timezone.timedelta(minutes=5)

        all_users = UserActivity.objects.filter(last_activity__gte=online_threshold)

        admin_users_count = all_users.filter(user__user_type="admin").count()
        ngo_users_count = all_users.filter(user__user_type="ngo").count()
        college_users_count = all_users.filter(user__user_type="college").count()
        students_users_count = all_users.filter(user__user_type="student").count()
        data = {
            "total_android_application_downloads": total_android_application_downloads,
            "total_student_memberships": total_student_memberships,
            "total_project_subscriptions": total_project_subscriptions,
            "subscription_expired_without_project_completion": subscription_expired_without_project_completion,
            "total_reports_generated": total_reports_generated,
            "admin_users_count": admin_users_count,
            "ngo_users_count": ngo_users_count,
            "college_users_count": college_users_count,
            "students_users_count": students_users_count,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class IncrementDownloadCount(APIView):
    def post(self, request, format=None):
        app_download, created = AppDownload.objects.get_or_create(pk=1)
        app_download.download_count += 1
        app_download.save()
        serializer = AppDownloadSerializer(app_download)
        return Response(serializer.data, status=status.HTTP_200_OK)
