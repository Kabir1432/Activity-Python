from django.utils import timezone
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from activityngo.entities.models import (Batches, Branch, Degree,
                                         ProjectCategory, ProjectType, State, ImplementationBatches)
from activityngo.entities.serializers import (BatchSerializer,
                                              BranchSerializer,
                                              DegreeSerializer,
                                              ProjectCategorySerializer,
                                              ProjectTypeSerializer,
                                              StateSerializer, ImplementationBatchesSerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAPIKEYAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = ('category__name', 'user__uuid')
    search_fields = ["name"]
    ordering = ["name", ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply ordering to the queryset if provided
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)
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
                    _(f"Pending Days of {90 - remaining_days} Days to delete the State")
                )
        else:
            raise ValidationError(_("Delete can happen only after 90 days of disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class DegreeViewSet(ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    permission_classes = [IsAPIKEYAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering = ["name", ]

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


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAPIKEYAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering = ["name", ]

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


class ProjectCategoryViewSet(ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
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
                    _(
                        f"Pending Days: {90 - remaining_days} to delete the Activity Category"
                    )
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectTypeViewSet(ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["type"]

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
                    _(f"Pending Days: {90 - remaining_days} to delete the Activity Type")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class BatchViewSet(ModelViewSet):
    queryset = Batches.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [IsAPIKEYAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["start_year", "end_year"]

    # search_fields = ["year"]
    # ordering = ["year", ]

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


class ImplementationBatchesViewSet(ModelViewSet):
    queryset = ImplementationBatches.objects.all()
    serializer_class = ImplementationBatchesSerializer
    permission_classes = [IsAPIKEYAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["start_year","end_year"]
    ordering = ["end_year", "start_year"]

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
