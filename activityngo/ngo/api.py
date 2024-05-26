from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from activityngo.ngo.models import (Bank, Directors, Franchise, Ngo, NgoCMS,
                                    NGOCollaboration, Organization,
                                    OrganizationAttachments)
from activityngo.ngo.renderer import OrganizationRenderer
from activityngo.ngo.serializers import (BankSerializer, DirectorSerializer,
                                         FranchiseSerializer, NgoCMSSerializer,
                                         NGOCollaborationSerializer,
                                         NgoSerializer,
                                         OrganizationAttachmentsSerializer,
                                         OrganizationSerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class NgoViewSet(viewsets.ModelViewSet):
    queryset = Ngo.objects.all()
    serializer_class = NgoSerializer
    # permission_classes = []
    #
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    )  #
    search_fields = [
        "ngo_name",
    ]
    ordering_fields = ["ngo_name", "state__name",]

    # lookup_field = 'id'
    # renderer_classes = [OrganizationRenderer]

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
                    _(f"Pending Days: {90 - remaining_days} to delete the NGO Profile")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class NGOCollaborationViewSet(viewsets.ModelViewSet):
    queryset = NGOCollaboration.objects.all()
    serializer_class = NGOCollaborationSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class NgoCMSDetail(DetailView):
    model = NGOCollaboration
    template_name = "cms/ngo_cms.html"


class FranchiseViewSet(viewsets.ModelViewSet):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = []

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        user_dict = {key: data[key] for key in ["email", "phone"]}
        request.data.pop("name", None)
        request.data.pop("name2", None)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        ngo = self.request.query_params.get("ngo")

        if ngo:
            try:
                ngo = int(ngo)
            except Exception as e:
                raise ValidationError(_("Value should be number"))

            return queryset.filter(ngo=ngo)
        return queryset


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = []
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    # lookup_field = 'id'
    # renderer_classes = [OrganizationRenderer]

    # def get_queryset(self):
    #     franchise = self.request.query_params.get('franchise')
    #     queryset = super().get_queryset()
    #     if self.request.user.is_superuser:
    #         return queryset.filter(user=self.request.user, user__is_superuser=True)
    #
    #     if franchise:
    #         try:
    #             franchise = int(franchise)
    #         except Exception as e:
    #             raise ValidationError(_("Value should be number"))
    #         return queryset.filter(~Q(franchise=None) & Q(user=None), franchise=franchise)
    #     return queryset.filter(~Q(franchise=None) & Q(user=None))


class DirectorsViewSet(viewsets.ModelViewSet):
    queryset = Directors.objects.all()
    serializer_class = DirectorSerializer
    # permission_classes = []
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]

    # def get_queryset(self):
    #     organization = self.request.query_params.get('organization')
    #     queryset = super().get_queryset()
    #     if self.request.user.is_superuser:
    #         return queryset.filter(organization__user=self.request.user, organization__user__is_superuser=True)
    #
    #     if organization:
    #         try:
    #             organization = int(organization)
    #         except Exception as e:
    #             raise ValidationError(_("Value should be number"))
    #         return queryset.filter(~Q(organization__franchise=None) & Q(organization__user=None), organization=organization)
    #     return queryset.filter(~Q(organization__franchise=None) & Q(organization__user=None))


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    # permission_classes = []
    permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]

    # def get_queryset(self):
    #     organization = self.request.query_params.get('organization')
    #     queryset = super().get_queryset()
    #     if self.request.user.is_superuser:
    #         return queryset.filter(organization__user=self.request.user, organization__user__is_superuser=True)
    #
    #     if organization:
    #         try:
    #             organization = int(organization)
    #         except Exception as e:
    #             raise ValidationError(_("Value should be number"))
    #         return queryset.filter(~Q(organization__franchise=None) & Q(organization__user=None), organization=organization)
    #     return queryset.filter(~Q(organization__franchise=None) & Q(organization__user=None))


class OrganizationAttachmentsViewSet(viewsets.ModelViewSet):
    queryset = OrganizationAttachments.objects.all()
    serializer_class = OrganizationAttachmentsSerializer
    permission_classes = []
    # permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]

    # def get_queryset(self):
    #     organization = self.request.query_params.get('organization')
    #     queryset = super().get_queryset()
    #     if self.request.user.is_superuser:
    #         return queryset.filter(organization__user=self.request.user, organization__user__is_superuser=True)
    #
    #     if organization:
    #         try:
    #             organization = int(organization)
    #         except Exception as e:
    #             raise ValidationError(_("Value should be number"))
    #         return queryset.filter(organization=organization)
    #     return queryset.filter(~Q(organization__franchise=None) & Q(organization__user=None))


class NgoCMSViewSet(viewsets.ModelViewSet):
    queryset = NgoCMS.objects.all()
    serializer_class = NgoCMSSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        "organization__franchise__ngo",
    ]

    # permission_classes = [IsAPIKEYAuthenticated, permissions.IsAuthenticated]
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.request.user.is_superuser:
    #         return queryset.filter(organization__user=self.request.user, organization__user__is_superuser=True)
    #     return queryset.filter(~Q(organization__franchise=None) & Q(organization__user=None))


class CMSDetail(DetailView):
    model = NgoCMS
    template_name = "cms/ngo_cms.html"
