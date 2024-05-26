from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from activityngo.website_content.models import WebsiteContent, WebsiteCoverPhoto
from activityngo.website_content.serializers import WebsiteContentSerializer, WebsiteCoverPhotoSerializer
from activityngo.utils.permissions import (
    IsAPIKEYAuthenticated,
    IsSuperAdminUser,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class WebsiteContentViewSet(viewsets.ModelViewSet):
    queryset = WebsiteContent.objects.all()
    serializer_class = WebsiteContentSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated, IsSuperAdminUser]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        "domain",
        "page_name",
    ]


class WebsiteCoverPhotoViewSet(viewsets.ModelViewSet):
    queryset = WebsiteCoverPhoto.objects.all()
    serializer_class = WebsiteCoverPhotoSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated, IsSuperAdminUser]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        "domain",
    ]
