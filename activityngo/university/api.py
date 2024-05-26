from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from activityngo.university.models import (University, UniversityCMS,
                                           UniversityCollaboration,
                                           UniversityRules)
from activityngo.university.serializers import (
    UniversityCMSSerializer, UniversityCollaborationSerializer,
    UniversityRulesSerializer, UniversitySerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsAPIKEYAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    search_fields = ["name"]
    ordering = ["name", "address"]

    def get_queryset(self):
        queryset = super().get_queryset()
        state_id = self.request.query_params.get("state_id")
        user = self.request.user
        if user.is_anonymous:
            queryset = queryset.filter(is_active=True, is_delete=False)
        else:
            if user.user_type == "student":
                queryset = queryset.filter(is_active=True, is_delete=False)

        if state_id:
            try:
                state_id = int(state_id)
                return queryset.filter(state__id=state_id)
            except Exception as e:
                raise ValidationError(_("Value should be number"))

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
                    _(f"PENDING DAYS: {90 - remaining_days} to delete the university")
                )
        else:
            raise ValidationError(_("Delete can be done only after 90 Days of Disable"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class UniversityCollaborationViewSet(viewsets.ModelViewSet):
    queryset = UniversityCollaboration.objects.all()
    serializer_class = UniversityCollaborationSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class UniversityCMSDetail(DetailView):
    model = UniversityCollaboration
    template_name = "cms/ngo_cms.html"


class UniversityRulesViewset(viewsets.ModelViewSet):
    queryset = UniversityRules.objects.all()
    serializer_class = UniversityRulesSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["university__name"]


class UniversityCMSViewSet(viewsets.ModelViewSet):
    queryset = UniversityCMS.objects.all()
    serializer_class = UniversityCMSSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class CMSDetail(DetailView):
    model = UniversityCMS
    template_name = "cms/cms.html"
