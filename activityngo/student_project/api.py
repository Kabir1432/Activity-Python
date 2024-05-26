from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activityngo.order.models import OrderDetail
from activityngo.project.models import Project
from activityngo.question_types.models import TaskInstructions
from activityngo.question_types.serializers import (
    DropdownQuestionSerializer, EssayQuestionSerializer,
    ExitTestQuestionSerializer, MCQQuestionSerializer,
    NumericQuestionSerializer, PercentageQuestionSerializer,
    ShortAnswerQuestionSerializer, UploadPhotoQuestionSerializer,
    VideoQuestionSerializer, TaskInstructionsSerializer)
from activityngo.student_project.models import (EssayQuestionAnswers,
                                                ExitQuestionAnswers,
                                                StudentTaskStatus,
                                                SurveysDetails)
from activityngo.student_project.renderer import SurveyTask3Renderer
from activityngo.student_project.serializer import (
    AnswersDropDownQuestionSerializer, AnswersEssayQuestionSerializer,
    AnswersExitQuestionSerializer, AnswersMCQQuestionSerializer,
    AnswersNumericQuestionSerializer, AnswersPercentageQuestionSerializer,
    AnswersShortQuestionSerializer, AnswersUploadPhotoQuestionSerializer,
    AnswersVideoQuestionSerializer, EmptyStudentProjectDetailsSerializer,
    StudentPurchaseProjectDetailsSerializer,
    StudentPurchaseProjectListSerializer, StudentTaskStatusSerializer,
    SurveysDetailsSerializer, SurveyTask3Serializer, SurveyTask9Serializer)
from activityngo.student_project.task_9_renderer import SubmitTask9Renderer
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class StudentProjectDetailsViewSet(viewsets.GenericViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    serializer_class = EmptyStudentProjectDetailsSerializer
    serializer_classes = {
        "purchase_project": StudentPurchaseProjectListSerializer,  # this is for on-going project list
        "purchase_project_details": StudentPurchaseProjectDetailsSerializer,
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
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="purchase-project",
    )
    def purchase_project(self, request, *args, **kwargs):
        is_ongoing_project = request.query_params.get("ongoing-project", False)

        queryset_filter = dict()
        if is_ongoing_project:
            queryset_filter = {"is_expire": False, "order__is_temp_order": False, "is_active": True}

        order_queryset = list(
            OrderDetail.objects.filter(
                order__user=request.user, order__is_active=1, **queryset_filter
            )
            .order_by("-id")
            .values_list("project", flat=True)
        )

        # Final result
        if order_queryset:
            ordering = "FIELD(`id`, {})".format(
                ",".join(str(id) for id in order_queryset)
            )
            queryset = Project.objects.filter(id__in=order_queryset).extra(
                select={"ordering": ordering}, order_by=("ordering",)
            )
        else:
            queryset = Project.objects.none()

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @transaction.atomic
    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="purchase-project-details",
    )
    def purchase_project_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(OrderDetail, id=order_id)
            data = StudentPurchaseProjectDetailsSerializer(
                order_details.project,
                context={
                    "order_details": order_details,
                    "request": request,
                    "number_of_points": order_details.number_of_points,
                },
            ).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-1-details",
    )
    def task_1_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )
            queryset = order_details.project.video_question_projects.filter(
                # is_active=1
            ).order_by("sub_task_number")[:2]
            print(queryset)
            data = dict()
            data["result"] = VideoQuestionSerializer(
                queryset,
                many=True,
                context={"request": request, "order_details": order_details},
            ).data
            data["order_id"] = order_id

            data["task_instruction"] = TaskInstructionsSerializer(
                TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_1"), many=True,
            ).data
            data[
                "total_hours"
            ] = order_details.project.task_instructions_question_projects.get(
                main_task_number="task_1"
            ).task_completed_hours
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-2-details",
    )
    def task_2_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )
            minus_limit = EssayQuestionAnswers.objects.filter(
                order_details=order_details, question__main_task_number="task_2"
            ).count()
            limits = 5 - minus_limit
            if order_details.number_of_points == "points_20":
                limits = 20 - minus_limit
            elif order_details.number_of_points == "points_10":
                limits = 10 - minus_limit

            queryset = (
                order_details.project.essay_question_projects.exclude(
                    id__in=list(
                        order_details.essay_question_order_details.filter(
                            user=request.user
                        ).values_list("question", flat=True)
                    )
                )
                .filter(is_active=1, main_task_number="task_2")
                .order_by("sub_task_number")[:limits]
            )
            data = dict()
            data["result"] = EssayQuestionSerializer(
                queryset,
                many=True,
                context={
                    "request": request,
                    "order_details": order_details,
                    "survey_number": 1,
                },
            ).data
            data["task_instruction"] = TaskInstructionsSerializer(
                TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_2"), many=True,
            ).data
            data["order_id"] = order_id
            total_questions = (
                20
                if order_details.number_of_points == "points_20"
                else 10
                if order_details.number_of_points == "points_10"
                else 5
            )
            data["total_questions"] = total_questions
            data[
                "total_hours"
            ] = order_details.project.task_instructions_question_projects.get(
                main_task_number="task_2"
            ).task_completed_hours
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-3-details",
    )
    def task_3_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )

            # total_completed_survey = order_details.task3_surveys_details_order_details.filter(
            #     user=request.user, main_task_number="task_3"
            # ).count()
            total_completed_survey = (
                order_details.student_task_status_order_details.task3_submissions
            )
            number_of_survey = 6
            if order_details.number_of_points == "points_20":
                number_of_survey = 10

            if number_of_survey != total_completed_survey:
                upload_photo_questions = UploadPhotoQuestionSerializer(
                    order_details.project.upload_photo_question_projects.filter(
                        is_active=1, main_task_number="task_3"
                    ).order_by("sub_task_number")[:1],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": total_completed_survey + 1,
                    },
                ).data
                short_answers_questions = ShortAnswerQuestionSerializer(
                    order_details.project.short_question_projects.filter(
                        is_active=1, main_task_number="task_3"
                    ).order_by("sub_task_number")[:1],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": total_completed_survey + 1,
                    },
                ).data
                numeric_questions = NumericQuestionSerializer(
                    order_details.project.numeric_question_projects.filter(
                        is_active=1, main_task_number="task_3"
                    ).order_by("sub_task_number")[:1],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": total_completed_survey + 1,
                    },
                ).data
                mcq_questions = MCQQuestionSerializer(
                    order_details.project.mcq_question_projects.filter(
                        is_active=1, main_task_number="task_3"
                    ).order_by("id")[:17],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": total_completed_survey + 1,
                    },
                ).data
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_3"),
                    many=True,
                ).data

                data = {
                    "upload_photo_questions": upload_photo_questions,
                    "short_answers_questions": short_answers_questions,
                    "numeric_questions": numeric_questions,
                    "mcq_questions": mcq_questions,
                    "number_of_survey": number_of_survey,
                    "total_completed_survey": total_completed_survey,
                    "task_instruction": task_instruction,
                    "order_id": order_id,
                    "total_questions": 20,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_3"
                    ).task_completed_hours,
                    "total_mcq_questions": 17,
                }
            else:
                data = {
                    "upload_photo_questions": [],
                    "short_answers_questions": [],
                    "numeric_questions": [],
                    "mcq_questions": [],
                    "task_instruction": [],
                    "number_of_survey": number_of_survey,
                    "total_completed_survey": total_completed_survey,
                    "order_id": order_id,
                    "total_hours": 0,
                    "total_questions": 20,
                    "total_mcq_questions": 17,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-4-details",
    )
    def task_4_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )
            if order_details.number_of_points == "points_05":
                queryset = (
                    order_details.project.exit_test_question_projects.exclude(
                        id__in=list(
                            order_details.exit_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_10")
                    .order_by("sub_task_number")[:20]
                )
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_10"),
                    many=True,
                ).data
                data = {
                    "exit_questions": ExitTestQuestionSerializer(
                        queryset,
                        many=True,
                        context={
                            "request": request,
                            "order_details": order_details,
                            "survey_number": 1,
                        },
                    ).data,
                    "order_id": order_id,
                    "total_questions": 20,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_10"
                    ).task_completed_hours,
                }
            else:
                upload_photo_questions = UploadPhotoQuestionSerializer(
                    order_details.project.upload_photo_question_projects.exclude(
                        id__in=list(
                            order_details.upload_photo_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_4")
                    .order_by("sub_task_number")[:3],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                short_answers_questions = ShortAnswerQuestionSerializer(
                    order_details.project.short_question_projects.exclude(
                        id__in=list(
                            order_details.short_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_4")
                    .order_by("sub_task_number")[:3],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                essay_answers_questions = EssayQuestionSerializer(
                    order_details.project.essay_question_projects.exclude(
                        id__in=list(
                            order_details.essay_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_4")
                    .order_by("sub_task_number")[:7],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_4"),
                    many=True,
                ).data
                data = {
                    "upload_photo_questions": upload_photo_questions,
                    "short_answers_questions": short_answers_questions,
                    "essay_answers_questions": essay_answers_questions,
                    "order_id": order_id,
                    "total_questions": 13,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_4"
                    ).task_completed_hours,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-5-details",
    )
    def task_5_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )

            if order_details.number_of_points == "points_05":
                data = dict()
            else:
                essay_answers_questions = EssayQuestionSerializer(
                    order_details.project.essay_question_projects.exclude(
                        id__in=list(
                            order_details.essay_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_5")
                    .order_by("sub_task_number")[:5],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_5"),
                    many=True,
                ).data
                data = {
                    "essay_answers_questions": essay_answers_questions,
                    "order_id": order_id,
                    "total_questions": 5,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_5"
                    ).task_completed_hours,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-6-details",
    )
    def task_6_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )

            if order_details.number_of_points == "points_05":
                data = dict()
            elif order_details.number_of_points == "points_10":
                queryset = (
                    order_details.project.exit_test_question_projects.exclude(
                        id__in=list(
                            order_details.exit_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_10")
                    .order_by("sub_task_number")[:20]
                )
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_10"),
                    many=True,
                ).data
                data = {
                    "exit_questions": ExitTestQuestionSerializer(
                        queryset,
                        many=True,
                        context={
                            "request": request,
                            "order_details": order_details,
                            "survey_number": 1,
                        },
                    ).data,
                    "order_id": order_id,
                    "total_questions": 20,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_10"
                    ).task_completed_hours,
                }
            else:
                essay_answers_questions = EssayQuestionSerializer(
                    order_details.project.essay_question_projects.exclude(
                        id__in=list(
                            order_details.essay_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_6")
                    .order_by("sub_task_number")[:5],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_6"),
                    many=True,
                ).data
                data = {
                    "essay_answers_questions": essay_answers_questions,
                    "order_id": order_id,
                    "total_questions": 5,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_6"
                    ).task_completed_hours,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-7-details",
    )
    def task_7_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )

            if order_details.number_of_points in ["points_05", "points_10"]:
                data = dict()
            else:
                essay_answers_questions = EssayQuestionSerializer(
                    order_details.project.essay_question_projects.exclude(
                        id__in=list(
                            order_details.essay_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_7")
                    .order_by("sub_task_number")[:5],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_7"),
                    many=True,
                ).data
                data = {
                    "essay_answers_questions": essay_answers_questions,
                    "order_id": order_id,
                    "total_questions": 5,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_7"
                    ).task_completed_hours,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-8-details",
    )
    def task_8_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )

            if order_details.number_of_points in ["points_05", "points_10"]:
                data = dict()
            else:
                essay_answers_questions = EssayQuestionSerializer(
                    order_details.project.essay_question_projects.exclude(
                        id__in=list(
                            order_details.essay_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_8")
                    .order_by("sub_task_number")[:5],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_8"),
                    many=True,
                ).data
                data = {
                    "essay_answers_questions": essay_answers_questions,
                    "order_id": order_id,
                    "total_questions": 5,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_8"
                    ).task_completed_hours,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-9-details",
    )
    def task_9_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )

            if order_details.number_of_points in ["points_05", "points_10"]:
                data = dict()
            else:
                short_answers_questions = ShortAnswerQuestionSerializer(
                    order_details.project.short_question_projects.exclude(
                        id__in=list(
                            order_details.short_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_9")
                    .order_by("sub_task_number")[:2],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                dropdown_answers_questions = DropdownQuestionSerializer(
                    order_details.project.dropdown_question_projects.exclude(
                        id__in=list(
                            order_details.dropdown_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_9")
                    .order_by("sub_task_number")[:2],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                numeric_questions = NumericQuestionSerializer(
                    order_details.project.numeric_question_projects.exclude(
                        id__in=list(
                            order_details.numeric_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_9")
                    .order_by("sub_task_number")[:17],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                percentage_questions = PercentageQuestionSerializer(
                    order_details.project.percentage_question_projects.exclude(
                        id__in=list(
                            order_details.percentage_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_9")
                    .order_by("sub_task_number")[:4],
                    many=True,
                    context={
                        "request": request,
                        "order_details": order_details,
                        "survey_number": 1,
                    },
                ).data
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_9"),
                    many=True,
                ).data
                data = {
                    "short_answers_questions": short_answers_questions,
                    "dropdown_answers_questions": dropdown_answers_questions,
                    "numeric_questions": numeric_questions,
                    "percentage_questions": percentage_questions,
                    "order_id": order_id,
                    "total_questions": 25,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_9"
                    ).task_completed_hours,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="task-10-details",
    )
    def task_10_details(self, request, *args, **kwargs):
        # Check if param_name exists in query parameters
        order_id = request.query_params.get("order_id", None)
        if order_id:
            order_details = get_object_or_404(
                OrderDetail, id=order_id, order__user=request.user, is_expire=False
            )

            if order_details.number_of_points in ["points_05", "points_10"]:
                data = dict()
            else:
                queryset = (
                    order_details.project.exit_test_question_projects.exclude(
                        id__in=list(
                            order_details.exit_question_order_details.filter(
                                user=request.user
                            ).values_list("question", flat=True)
                        )
                    )
                    .filter(is_active=1, main_task_number="task_10")
                    .order_by("sub_task_number")[:20]
                )
                task_instruction = TaskInstructionsSerializer(
                    TaskInstructions.objects.filter(project=order_details.project, main_task_number="task_10"),
                    many=True,
                ).data
                data = {
                    "exit_questions": ExitTestQuestionSerializer(
                        queryset,
                        many=True,
                        context={
                            "request": request,
                            "order_details": order_details,
                            "survey_number": 1,
                        },
                    ).data,
                    "order_id": order_id,
                    "total_questions": 20,
                    "task_instruction": task_instruction,
                    "total_hours": order_details.project.task_instructions_question_projects.get(
                        main_task_number="task_10"
                    ).task_completed_hours,
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "order_id is missing"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


class StudentAnswersViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    serializer_class = EmptyStudentProjectDetailsSerializer
    serializer_classes = {
        "video_question": AnswersVideoQuestionSerializer,
        "essay_question": AnswersEssayQuestionSerializer,
        "upload_photo_question": AnswersUploadPhotoQuestionSerializer,
        "short_question": AnswersShortQuestionSerializer,
        "numeric_question": AnswersNumericQuestionSerializer,
        "dropdown_question": AnswersDropDownQuestionSerializer,
        "percentage_question": AnswersPercentageQuestionSerializer,
        "mcq_question": AnswersMCQQuestionSerializer,
        "exit_question": AnswersExitQuestionSerializer,
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
        url_path="video-question",
    )
    def video_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="essay-question",
    )
    def essay_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="upload-photo-question",
    )
    def upload_photo_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="short-question",
    )
    def short_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="numeric-question",
    )
    def numeric_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="dropdown-question",
    )
    def dropdown_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="percentage-question",
    )
    def percentage_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="mcq-question",
    )
    def mcq_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated],
        url_path="exit-question",
    )
    def exit_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )


class SurveysDetailsViewSet(viewsets.ModelViewSet):
    queryset = SurveysDetails.objects.all()
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    serializer_class = SurveysDetailsSerializer


class StudentTaskStatusViewSet(viewsets.ModelViewSet):
    queryset = StudentTaskStatus.objects.all()
    serializer_class = StudentTaskStatusSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            if (
                    (
                            instance.order_details.number_of_points == "points_20"
                            and request.data.get("task10") == "submitted_for_evaluation"
                    )
                    or (
                    instance.order_details.number_of_points == "points_10"
                    and request.data.get("task6") == "submitted_for_evaluation"
            )
                    or (
                    instance.order_details.number_of_points == "points_05"
                    and request.data.get("task4") == "submitted_for_evaluation"
            )
            ):
                task_number = 10 if instance.order_details.number_of_points == "points_20" else 6 if instance.order_details.number_of_points == "points_10" else 4
                submit_question_queryset = ExitQuestionAnswers.objects.filter(
                    order_details=instance.order_details, status="Submitted"
                ).order_by("question__sub_task_number")
                ans_list = []
                for submit_question in submit_question_queryset:
                    correct_ans = (
                        submit_question.question.exit_test_question_option.filter(
                            right_answer_option_among_multiple_choice=True
                        )
                    )
                    if correct_ans.filter(pk=submit_question.answer.pk).exists():
                        submit_question.status = "Accepted"
                        ans_list.append(True)
                    else:
                        submit_question.status = "Rejected"
                        ans_list.append(False)
                    submit_question.save()
                if all(ans_list):
                    request.data[f"task{task_number}"] = "all_answers_are_accepted"
                else:
                    request.data[f"task{task_number}"] = "answer_rejected_in_evaluation"
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyTask3ViewSet(APIView):
    renderer_classes = [SurveyTask3Renderer]
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]

    @transaction.atomic
    # @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated, IsAPIKEYAuthenticated],
    #         url_path="task-3-survey", )
    def post(self, request, *args, **kwargs):
        serializer = SurveyTask3Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        short_question = request.data.get("short_question")
        numeric_question = request.data.get("numeric_question")
        mcq_question = request.data.get("mcq_question")

        # Submit single Short answers
        serializer = AnswersShortQuestionSerializer(
            data=short_question, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Submit single Numeric answers
        serializer = AnswersNumericQuestionSerializer(
            data=numeric_question, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Submit Multiple mcq answers
        serializer = AnswersMCQQuestionSerializer(
            data=mcq_question, many=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )


class SubmitTask9ViewSet(APIView):
    renderer_classes = [SubmitTask9Renderer]
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = SurveyTask9Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        short_question = request.data.get("short_question")
        dropdown_question = request.data.get("dropdown_question")
        numeric_question = request.data.get("numeric_question")
        percentage_question = request.data.get("percentage_question")

        # Submit Multiple Short answers
        serializer = AnswersShortQuestionSerializer(
            data=short_question, many=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Submit Multiple dropdown_question
        serializer = AnswersDropDownQuestionSerializer(
            data=dropdown_question, many=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Submit Multiple Numeric answers
        serializer = AnswersNumericQuestionSerializer(
            data=numeric_question, many=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Submit Multiple percentage_question
        serializer = AnswersPercentageQuestionSerializer(
            data=percentage_question, many=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"data": "task was submitted successfully!"}, status=status.HTTP_200_OK
        )
