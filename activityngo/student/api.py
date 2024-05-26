import json
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import (FileUploadParser, FormParser,
                                    MultiPartParser)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from activityngo.custom_auth.models import ApplicationUser, MultiToken
from activityngo.notification.FCM_manager import (subscribe_to_topic,
                                                  unsubscribe_from_topic)
from activityngo.student.models import (AboutUs, AicteRules, Complaints,
                                        ComplaintsMedia, Implementation,
                                        Necessity, OurTeam, StudentDetails,
                                        TermsAndCondition)
from activityngo.student.renderer import StudentRenderer
from activityngo.student.serializer import (AboutUsSerializer,
                                            AicteRulesSerializer,
                                            ComplaintsMediaSerializer,
                                            ComplaintsSerializer,
                                            ImplementationSerializer,
                                            NecessitySerializer,
                                            OurTeamSerializer,
                                            StudentChangePasswordSerializer,
                                            StudentDetailsEmptySerializer,
                                            StudentDetailsSerializer,
                                            StudentLoginSerializer,
                                            StudentSerializer,
                                            StudentSignUpSerializer,
                                            TermsAndConditionSerializer,
                                            UserSerializer, GrammarCheckSerializer)
# from activityngo.utils.email_send import sing_up_successful
from activityngo.utils.permissions import IsAPIKEYAuthenticated, IsStudentUser
from spellchecker import SpellChecker
from rest_framework.exceptions import ValidationError
from activityngo.utils.sendgrid_email_send import sing_up_successful


class StudentViewSet(viewsets.GenericViewSet):
    queryset = StudentDetails.objects.all()
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    serializer_class = StudentDetailsEmptySerializer
    serializer_classes = {
        "signup": StudentSignUpSerializer,
        "login": StudentLoginSerializer,
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="signup",
    )
    def signup(self, request, *args, **kwargs):
        """
        SIGNUP: user registration
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        sing_up_successful(user.student, request.data.get("password"))
        # For generate New auth token
        token = MultiToken.objects.create(user=user.student)

        data = StudentDetailsSerializer(user).data
        data["token"] = token.key

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], permission_classes=[IsAPIKEYAuthenticated])
    def login(self, request, *args, **kwargs):
        """
        defined user login API
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        device_type = serializer.validated_data.pop("device_type", None)
        device_token = serializer.validated_data.pop("device_token", None)
        device_id = serializer.validated_data.pop("device_id", None)
        os_version = serializer.validated_data.pop("os_version", None)
        device_name = serializer.validated_data.pop("device_name", None)
        model_name = serializer.validated_data.pop("model_name", None)
        ip_address = serializer.validated_data.pop("ip_address", None)
        uuid_number = serializer.validated_data.pop("uuid_number", None)
        imei_number = serializer.validated_data.pop("imei_number", None)
        app_version = serializer.validated_data.pop("app_version", None)
        api_version = serializer.validated_data.pop("api_version", None)

        user.tokens.all().delete()

        # For generate New auth token
        token = MultiToken.objects.create(user=user)

        # Update user details
        user.device_type = device_type
        user.device_token = device_token
        user.device_id = device_id
        user.os_version = os_version
        user.device_name = device_name
        user.model_name = model_name
        user.ip_address = ip_address
        user.uuid_number = uuid_number
        user.imei_number = imei_number
        user.app_version = app_version
        user.api_version = api_version
        user.save()

        # data = StudentSerializer(user).data
        data = StudentDetailsSerializer(user.student_details).data
        data["token"] = token.key

        # For Unsubscribe device token
        try:
            unsubscribe_from_topic(
                topic="admin_channel", registration_token=user.device_token
            )
        except:
            pass

        # for push notification
        subscribe_to_topic(topic="admin_channel", registration_token=user.device_token)

        return Response(data, status=status.HTTP_200_OK)


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class TermsConditionViewSet(viewsets.ModelViewSet):
    queryset = TermsAndCondition.objects.all()
    serializer_class = TermsAndConditionSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class OurTeamViewSet(viewsets.ModelViewSet):
    queryset = OurTeam.objects.all()
    serializer_class = OurTeamSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class NecessityViewSet(viewsets.ModelViewSet):
    queryset = Necessity.objects.all()
    serializer_class = NecessitySerializer
    permission_classes = [IsAPIKEYAuthenticated]


class AicteRulesViewSet(viewsets.ModelViewSet):
    queryset = AicteRules.objects.all()
    serializer_class = AicteRulesSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class ImplementationMethodViewSet(viewsets.ModelViewSet):
    queryset = Implementation.objects.all()
    serializer_class = ImplementationSerializer
    permission_classes = [IsAPIKEYAuthenticated]


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaints.objects.all()
    serializer_class = ComplaintsSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ["user__student_details__student_membership_id", "create_time", "user__fullname"]
    filterset_fields = ['status',]

    # def get_permissions(self):
    #     if self.action == 'create':
    #         # Use the custom permission class for creating orders
    #         return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsStudentUser()]
    #     return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.user_type == "student":
            return queryset.filter(user=user).order_by("-create_time")
        elif user.user_type == "admin":
            return queryset.order_by("-create_time")
        elif user.user_type == "sub_admin":
            return queryset.filter(allotted_to=user.user_subAdmin).order_by(
                "-create_time"
            )
        return queryset.order_by("-create_time")


class StudentDetailsViewSet(viewsets.ModelViewSet):
    queryset = StudentDetails.objects.all()
    serializer_class = StudentDetailsSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    renderer_classes = [StudentRenderer]
    filterset_fields = ["university", ]
    search_fields = ("student__fullname", "student_membership_id", "student__email")
    ordering_fields = ["student__fullname", "student_membership_id", "college__name"]
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_delete=False)
        return queryset.order_by("-create_time")

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        email = (
            request.data.get("student").get("email")
            if request.data.get("student")
            else False
        )
        phone = (
            request.data.get("student").get("phone")
            if request.data.get("student")
            else False
        )
        if (
                email
                and ApplicationUser.objects.exclude(pk=instance.student.pk)
                .filter(email=email)
                .exists()
        ):
            return Response(
                {"email": ["A user with that email already exists."]}, status=400
            )
        elif email and email == instance.student.email:
            data = request.data.get("student").pop("email")

        if (
                phone
                and ApplicationUser.objects.exclude(pk=instance.student.pk)
                .filter(phone=phone)
                .exists()
        ):
            return Response(
                {"phone": ["A user with that phone already exists."]}, status=400
            )
        elif phone and phone == instance.student.phone:
            data = request.data.get("student").pop("phone")
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(
        methods=["post"],
        detail=False,
        url_path="change-password",
        url_name="change_password",
    )
    def change_password(self, request, *args, **kwargs):
        serializer = StudentChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(StudentDetails, pk=serializer.data.get("student_id"))
        user = user.student
        user.set_password(serializer.data["new_password"])
        user.save()
        return Response(_("Password update successfully!"))


class ComplaintMediaViewSet(viewsets.ModelViewSet):
    queryset = ComplaintsMedia.objects.all()
    serializer_class = ComplaintsMediaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    related_model = Complaints


class GrammarCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]

    @staticmethod
    def correct_spelling(input_text):
        # Split the input text into words
        spell = SpellChecker()
        word_list = input_text.split()
        filtered_words = [word for word in word_list if len(word) <= 20]
        # Find misspelled words
        misspelled_words = spell.unknown(filtered_words)

        corrections_list = []

        for word in misspelled_words:
            correction = {
                "incorrect_word": word,
                "correct_word": spell.correction(word)
            }

            corrections_list.append(correction)

        return corrections_list

    def post(self, request, *args, **kwargs):
        serializer = GrammarCheckSerializer(data=request.data)

        if serializer.is_valid():
            grammar_check = serializer.validated_data['grammar_check']
            correct_spelling_list = self.correct_spelling(grammar_check)

            if correct_spelling_list:

                return Response({'correct_spelling': correct_spelling_list, "length": len(correct_spelling_list)},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "correct_spelling": [
                        {
                            "incorrect_word": None,
                            "correct_word": None
                        }
                    ],
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
