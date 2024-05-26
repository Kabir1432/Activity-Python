from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from activityngo.cms.models import (
    CMS,
    FAQ,
    ContactUS,
    ContactUSForm,
    UserManual,
    MyCartInstructions,
)
from activityngo.cms.serializers import (
    CMSSerializer,
    ContactUSFormSerializer,
    ContactUSSerializer,
    FAQSerializer,
    UserManualSerializer,
    MyCartInstructionsSerializer,
)
from activityngo.utils.permissions import (
    IsAPIKEYAuthenticated,
    IsStudentUser,
    IsSuperAdminUser,
)


class CMSDetail(DetailView):
    model = CMS
    template_name = "cms/main_cms.html"


class CMSViewSet(viewsets.ModelViewSet):
    queryset = CMS.objects.all()
    serializer_class = CMSSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        "meta_key",
    ]
    lookup_field = "id"

    # def get_permissions(self):
    #     if self.action == 'create':
    #         # Use the custom permission class for creating orders
    #         return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsSuperAdminUser()]
    #     return super().get_permissions()


class UserManualViewSet(viewsets.ModelViewSet):
    queryset = UserManual.objects.all()
    serializer_class = UserManualSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    lookup_field = "id"

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("its working")
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == "create":
            # Use the custom permission class for creating orders
            return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsSuperAdminUser()]
        return super().get_permissions()


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [
        IsAuthenticated,
        IsAPIKEYAuthenticated,
    ]

    # def get_permissions(self):
    #     if self.request.user.user_type == 'student' and self.action == 'list':
    #         return [IsAuthenticated(), IsAPIKEYAuthenticated(), ]
    #     return super().get_permissions()


class ContactUSFormViewSet(viewsets.ModelViewSet):
    queryset = ContactUSForm.objects.all()
    serializer_class = ContactUSFormSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated, IsSuperAdminUser]

    def get_queryset(self):
        if self.request.method in ["POST", "DELETE", "GET"]:
            # Only allow POST and DELETE requests to access the queryset
            return ContactUSForm.objects.all()
        raise exceptions.MethodNotAllowed(self.request.method)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsStudentUser()]
        return super().get_permissions()

    # def get_queryset(self):
    #     if self.request.method in ['POST', 'DELETE', 'GET']:
    #         # Only allow POST and DELETE requests to access the queryset
    #         return ContactUSForm.objects.all()
    #     raise Http405MethodNotAllowed


class ContactUSViewSet(viewsets.ModelViewSet):
    queryset = ContactUS.objects.all()
    serializer_class = ContactUSSerializer
    permission_classes = [
        IsAuthenticated,
        IsAPIKEYAuthenticated,
    ]

    def get_queryset(self):
        print(self.request.method)
        if self.request.method not in [
            "DELETE",
        ]:
            # Only allow POST and DELETE requests to access the queryset
            return ContactUS.objects.all()
        raise exceptions.MethodNotAllowed(self.request.method)

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsStudentUser()]
    #     return super().get_permissions()


class MyCartInstructionsViewSet(viewsets.ModelViewSet):
    queryset = MyCartInstructions.objects.all()
    serializer_class = MyCartInstructionsSerializer
    permission_classes = [
        IsAuthenticated,
        IsAPIKEYAuthenticated,
    ]

    def get_queryset(self):
        if self.request.method not in [
            "DELETE",
        ]:
            # Only allow POST and DELETE requests to access the queryset
            return MyCartInstructions.objects.all()
        raise exceptions.MethodNotAllowed(self.request.method)
