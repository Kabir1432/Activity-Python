from datetime import datetime
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.utils.translation import gettext as _
from activityngo.activity_report.models import ReportContent
from activityngo.activity_report.serializers import ReportContentSerializer
from activityngo.college.models import College
from activityngo.entities.models import State
from activityngo.ngo.models import Ngo
from activityngo.order.models import OrderDetail
from activityngo.project.models import Project
from activityngo.student.models import StudentDetails
from activityngo.university.models import University
from activityngo.utils.permissions import (
    IsAPIKEYAuthenticated,
    IsStudentUser,
    IsSuperAdminUser,
)
from rest_framework.exceptions import ValidationError


class ReportContentSet(ModelViewSet):
    queryset = ReportContent.objects.all()
    serializer_class = ReportContentSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["project__id", "type_point"]
    search_fields = ["project__title",]
    ordering_fields = ["project__title", "project__franchise_ngo_name__ngo_name"]

    # def get_permissions(self):
    #     if self.action == 'create':
    #         # Use the custom permission class for creating orders
    #         return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsStudentUser()]
    #     return super().get_permissions()

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     user = self.request.user
    #     if user.user_type == 'student':
    #         return queryset.filter(user=user).order_by('-create_time')
    #     return queryset.order_by('-create_time')
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
                    _(f"PENDING DAYS: {90 - remaining_days} to delete the batch")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetStatisticsViewSet(APIView):
    permission_classes = []  # IsAPIKEYAuthenticated, IsAuthenticated

    def get(self, request):
        registered_students = StudentDetails.objects.all().count()
        subscribed_projects = OrderDetail.objects.all().count()
        available_projects = Project.objects.all().count()
        colleges = College.objects.all().count()
        universities = University.objects.all().count()
        states = State.objects.all().count()
        available_ngos = Ngo.objects.all().count()

        year = request.query_params.get("year")
        try:
            if year is not None:
                year = int(year)
                if not 1500 <= year <= 2300:
                    return Response({"error": "year is wrong."}, status=400)
        except ValueError:
            return Response({"error": "year must be integers."}, status=400)

        filter_registered_students = (
            StudentDetails.objects.filter(create_time__year=year).count()
            if year
            else registered_students
        )
        filter_subscribed_projects = (
            OrderDetail.objects.filter(create_time__year=year).count()
            if year
            else subscribed_projects
        )
        filter_available_projects = (
            Project.objects.filter(create_time__year=year).count()
            if year
            else available_projects
        )
        filter_colleges = (
            College.objects.filter(create_time__year=year).count() if year else colleges
        )
        filter_universities = (
            University.objects.filter(create_time__year=year).count()
            if year
            else universities
        )
        filter_states = (
            State.objects.filter(create_time__year=year).count() if year else states
        )
        filter_available_ngos = (
            Ngo.objects.filter(create_time__year=year).count()
            if year
            else available_ngos
        )

        response_data = {
            "today_date": datetime.now(),
            "registered_students:": registered_students,
            "subscribed_projects:": subscribed_projects,
            "available_projects:": available_projects,
            "colleges": colleges,
            "universities": universities,
            "states": states,
            "available_ngos": available_ngos,
            "filter_registered_students:": filter_registered_students,
            "filter_subscribed_projects:": filter_subscribed_projects,
            "filter_available_projects:": filter_available_projects,
            "filter_colleges": filter_colleges,
            "filter_universities": filter_universities,
            "filter_states": filter_states,
            "filter_available_ngos": filter_available_ngos,
        }

        return Response(response_data, status=status.HTTP_200_OK)
