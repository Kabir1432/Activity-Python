from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from activityngo.college.models import (
    BranchBatches,
    College,
    CollegeCMS,
    CollegeCollaboration,
    CollegeDegree,
    CollegeUsers,
    DegreeBranch,
)
from activityngo.college.renderer import CollegeBatchesRenderer, CollegeUserRenderer
from activityngo.college.serializers import (
    BranchBatchesSerializer,
    CollegeCMSSerializer,
    CollegeCollaborationSerializer,
    CollegeDegreeSerializer,
    CollegeListSerializer,
    CollegeSerializer,
    CollegeUsersSerializer,
    DegreeBranchSerializer,
)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class CollegeViewSet(ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [IsAPIKEYAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering = ["name", "address", "state__name", "university__name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        university_id = self.request.query_params.get("university_id")
        user = self.request.user
        if user.is_anonymous:
            queryset = queryset.filter(is_active=True, is_delete=False)
        else:
            if user.user_type == "student":
                queryset = queryset.filter(is_active=True, is_delete=False)

        if university_id:
            try:
                university_id = int(university_id)
                return queryset.filter(university__id=university_id)
            except Exception as e:
                raise ValidationError(_("Value should be number"))

        return queryset

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return CollegeListSerializer
    #
    #     return super().get_serializer_class()

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
                    _(f"PENDING DAYS: {90 - remaining_days} to delete the college")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollegeDegreeViewSet(viewsets.ModelViewSet):
    queryset = CollegeDegree.objects.all()
    serializer_class = CollegeDegreeSerializer
    permission_classes = [
        IsAPIKEYAuthenticated,
    ]
    filterset_fields = ["college"]

    # filterset_fields = ['college']
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_anonymous:
            queryset = queryset.filter(is_active=True, is_delete=False)
        else:
            if user.user_type == "student":
                queryset = queryset.filter(is_active=True, is_delete=False)
        return queryset

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
                    _(f"PENDING DAYS: {90 - remaining_days} to delete the degree")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class DegreeBranchViewSet(viewsets.ModelViewSet):
    queryset = DegreeBranch.objects.all()
    serializer_class = DegreeBranchSerializer
    permission_classes = [
        IsAPIKEYAuthenticated,
    ]
    filterset_fields = ["college_degree"]

    # filterset_fields = ['college']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_anonymous:
            queryset = queryset.filter(is_active=True, is_delete=False)
        else:
            if user.user_type == "student":
                queryset = queryset.filter(is_active=True, is_delete=False)
        return queryset

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
                    _(f"PENDING DAYS: {90 - remaining_days} to delete the branch")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class BranchBatchesViewSet(viewsets.ModelViewSet):
    queryset = BranchBatches.objects.all()
    serializer_class = BranchBatchesSerializer
    permission_classes = [
        IsAPIKEYAuthenticated,
    ]
    filterset_fields = ["degree_branch"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_anonymous:
            queryset = queryset.filter(is_active=True, is_delete=False)
        else:
            if user.user_type == "student":
                queryset = queryset.filter(is_active=True, is_delete=False)
        return queryset

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


class CollegeCollaborationViewSet(viewsets.ModelViewSet):
    queryset = CollegeCollaboration.objects.all()
    serializer_class = CollegeCollaborationSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class CollegeCMSDetail(DetailView):
    model = CollegeCollaboration
    template_name = "cms/ngo_cms.html"


class CollegeUsersViewSet(ModelViewSet):
    queryset = CollegeUsers.objects.all()
    serializer_class = CollegeUsersSerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    renderer_classes = [CollegeUserRenderer]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["user__username"]
    ordering_fields = [
        "user__username",
        "college__name",
        "branch__branch__name",
    ]

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
                    _(
                        f"Pending Days of {90 - remaining_days} to delete the college user profile"
                    )
                )
        else:
            raise ValidationError(_("Delete can happen only after 90 days of disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollegeCMSViewSet(viewsets.ModelViewSet):
    queryset = CollegeCMS.objects.all()
    serializer_class = CollegeCMSSerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]


class CMSDetail(DetailView):
    model = CollegeCMS
    template_name = "cms/cms.html"
