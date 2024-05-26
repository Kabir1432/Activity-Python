from django.db.models import Avg, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from activityngo.project.models import (Project, ProjectDetails, SpecialPower,
                                        StudentFeedback)
from activityngo.project.serializers import (ProjectDetailsSerializer,
                                             ProjectListSerializer,
                                             ProjectSerializer,
                                             SpecialPowerSerializer,
                                             StudentFeedbackSerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("-id")
    serializer_class = ProjectSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )  #
    search_fields = [
        "title",
    ]
    filterset_fields = ["category", "franchise_ngo_name"]
    ordering_fields = ["price", "title", "-title", "purchase_count", "price_of_20_point"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.user_type == "student" and not user.is_superuser:
            queryset = queryset.filter(is_visible=True, is_active=True)
            # special_power = SpecialPower.objects.filter(
            #     project__id__in=queryset.values_list("id", flat=True),
            #     state=user.student_details.student_state,
            #     university=user.student_details.university,
            #     college=user.student_details.college,
            #     degree=user.student_details.degree,
            #     batch=user.student_details.batch,
            # ).values_list("project_id", flat=True)
            # # return queryset.filter(id__in=special_power)
            #
            # if len(special_power) == 0:
            #     project_id = SpecialPower.objects.filter(is_active=True).values_list(
            #         "project_id", flat=True
            #     )
            #     # return queryset.exclude(id__in=project_id)
            #     queryset = queryset.exclude(id__in=project_id)
            # else:
            #     project_id = SpecialPower.objects.exclude(
            #         project_id__in=special_power, is_active=False
            #     ).values_list("project_id", flat=True)
            #     # return queryset.filter(id__in=project_id)
            #     queryset = queryset.filter(id__in=project_id)

        ordering = self.request.query_params.get("ordering")

        if ordering == "price_asc":
            queryset = queryset.order_by("price_of_20_point")
        elif ordering == "price_desc":
            queryset = queryset.order_by("-price_of_20_point")

            # Add custom ordering by most purchased
        if ordering == "most_purchased":
            queryset = queryset.annotate(
                purchase_count=Count("product_order_details")
            ).order_by("-purchase_count")

        most_rating = self.request.query_params.get("most_rating")

        if most_rating:
            # queryset = Project.objects.annotate(
            #     average_rating=Avg("projects_feedback__rating")
            # )
            queryset = queryset.annotate(
                average_rating=Avg("projects_feedback__rating")
            )
            queryset = queryset.order_by("-average_rating")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update is_active status By Default F  alse
        serializer.validated_data["is_active"] = False

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ProjectDetailsViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetails.objects.all()
    serializer_class = ProjectDetailsSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]


class StudentFeedbackViewSet(viewsets.ModelViewSet):
    queryset = StudentFeedback.objects.all()
    serializer_class = StudentFeedbackSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ["project__title", "rating", "feedback"]


class SpecialPowerViewSet(viewsets.ModelViewSet):
    queryset = SpecialPower.objects.all()
    serializer_class = SpecialPowerSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
