from django.apps import apps
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from activityngo.order.models import OrderDetail
from activityngo.project.models import Project
from activityngo.question_types.models import (DropdownQuestion, EssayQuestion,
                                               NumericQuestion,
                                               PercentageQuestion,
                                               ShortAnswerQuestion,
                                               UploadPhotoQuestion)
from activityngo.student_project.models import (DropDownQuestionAnswers,
                                                EssayQuestionAnswers,
                                                MCQQuestionAnswers,
                                                NumericQuestionAnswers,
                                                PercentageQuestionAnswers,
                                                ShortQuestionAnswers,
                                                StudentTaskStatus,
                                                UploadPhotoQuestionAnswers)
from activityngo.task_evaluation.paginator import \
    EssayEvaluationQuestionPagination
from activityngo.task_evaluation.serializers import (
    DropDownQuestionAnswersSerializer, EssayQuestionAnswersSerializer,
    EvaluationEssayQuestionSerializer, EvaluationFor05PointProjectSerializer,
    EvaluationFor10PointProjectSerializer,
    EvaluationFor20PointProjectSerializer, EvaluationQuestionAnswersSerializer,
    EvaluationResultSerializer, EvaluationShortAnswerQuestionSerializer,
    EvaluationUploadPhotoQuestionSerializer,
    GetEssayEvaluationQuestionSerializer, NumericQuestionAnswersSerializer,
    OrderDetailSerializer, ShortQuestionAnswersSerializer,
    Task3McqQuestionSerializer, Task3PhotoQuestionSerializer,
    Task4EvaluationQuestionSerializer, UploadPhotoQuestionAnswersSerializer,
    create_dynamic_serializer, EditEvaluationAnswersSerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


# ----------------below api for get admin evaluation main admin listing --------------------
class EvaluationFor05PointProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by("-id")
    serializer_class = EvaluationFor05PointProjectSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    )
    search_fields = [
        "title",
    ]
    ordering_fields = ["title", ]

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="evaluation-for-05-point-task-details",
    )
    def evaluation_for_05_point_task_details(self, request, *args, **kwargs):
        order_details_param = request.GET.get("order_details")
        # Check if the 'project' parameter is present and if it's an integer
        if order_details_param is not None:
            try:
                order_details_param = int(order_details_param)
            except ValueError:
                return Response(
                    {
                        "error": "Invalid 'order_details' parameter. It must be an integer."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = EssayQuestionAnswers.objects.filter(
                order_details_id=order_details_param,
                question__main_task_number="task_2",
            )
            page = self.paginate_queryset(queryset)
            serializer = EssayQuestionAnswersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            {"error": "'order_details_param' parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EvaluationFor10PointProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by("-id")
    serializer_class = EvaluationFor10PointProjectSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    )
    search_fields = [
        "title",
    ]
    ordering_fields = ["title", ]

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="evaluation-for-05-point-task-details",
    )
    def evaluation_for_05_point_task_details(self, request, *args, **kwargs):
        order_details_param = request.GET.get("order_details")
        # Check if the 'project' parameter is present and if it's an integer
        if order_details_param is not None:
            try:
                order_details_param = int(order_details_param)
            except ValueError:
                return Response(
                    {
                        "error": "Invalid 'order_details' parameter. It must be an integer."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = EssayQuestionAnswers.objects.filter(
                order_details_id=order_details_param,
                question__main_task_number="task_2",
            )
            page = self.paginate_queryset(queryset)
            serializer = EssayQuestionAnswersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            {"error": "'order_details_param' parameter is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # @transaction.atomic
    # @action(methods=['post'], detail=False, url_path='submit-task-2', url_name='submit_task_2')
    # def submit_task_2(self, request, *args, **kwargs):
    #     serializer = SubmitTask02Serializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         essay_question_answers = serializer.data['essay_question_answers']
    #         status_of_answers = serializer.data['status']
    #         try:
    #             obj = EssayQuestionAnswers.objects.get(id=essay_question_answers)
    #         except EssayQuestionAnswers.DoesNotExist:
    #             return Response({"error": "Essay Question Don't exists with this id."}, status=404)
    #         obj.status = status_of_answers
    #         obj.save()
    #         return Response({"success": "task status updated"}, status=status.HTTP_201_CREATED)
    #
    #     except Exception as e:
    #         return Response({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class EvaluationFor20PointProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by("-id")
    serializer_class = EvaluationFor20PointProjectSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    )
    search_fields = [
        "title",
    ]
    ordering_fields = ["title", ]


# ------------------------below api for get details about the like project and get student for that project -----------
class DynamicEvaluationViewSet(viewsets.ReadOnlyModelViewSet):
    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="dynamic-evaluation-details",
    )
    def dynamic_evaluation_details(
            self, request, *args, **kwargs
    ):  # this is evaluation for admin for view details
        project_param = request.GET.get("project")
        number_of_points = request.GET.get("number_of_points")
        task_number = request.GET.get("task_number")
        student_name = request.query_params.get("student_name")  # This param for search
        # Check if the 'project' parameter is present and if it's an integer
        if (
                project_param is not None
                and number_of_points is not None
                and task_number is not None
        ):
            try:
                project_param = int(project_param)
            except ValueError:
                return Response(
                    {"error": "Invalid 'project' parameter. It must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = OrderDetail.objects.filter(
                project_id=project_param,
                number_of_points=number_of_points,
                is_expire=False,
            )
            if student_name:
                queryset = queryset.filter(
                    order__user__fullname__icontains=student_name
                )
            custom_task_number = {
                "task_1": "task1",
                "task_2": "task2",
                "task_3": "task3",
                "task_4": "task4",
                "task_5": "task5",
                "task_6": "task6",
                "task_7": "task7",
                "task_8": "task8",
                "task_9": "task9",
                "task_10": "task10",
            }

            filter_dict = {
                f"{custom_task_number.get(task_number)}": "submitted_for_evaluation",
            }

            complete_status = StudentTaskStatus.objects.filter(
                order_details__project_id=project_param,
                order_details__is_expire=False,
                order_details__number_of_points=number_of_points,
            )
            complete_status_list = complete_status.filter(**filter_dict).values_list(
                "order_details_id", flat=True
            )
            queryset = queryset.filter(pk__in=complete_status_list)

            project = Project.objects.get(id=project_param)
            page = self.paginate_queryset(queryset)
            serializer = OrderDetailSerializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            task_name = project.task_instructions_question_projects.filter(main_task_number=task_number).first()

            response.data.update({"task_number": task_number})
            response.data.update({"project_name": project.title})
            response.data.update({"project_type": project.type.name if project.type else None})
            response.data.update({"task_name": task_name.task_instructions if task_name else None})
            return response

        return Response(
            {
                "error": "'project', 'number_of_points' and 'task_number' parameter is required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="get-dynamic-essay-evaluation-question",
    )
    def get_dynamic_essay_evaluation_question_question(self, request, *args, **kwargs):
        # this help to get data of task_2, task_5,task_6,task_7 and task_8 for more information view serializer
        serializer = GetEssayEvaluationQuestionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order_details = serializer.data.get("order_details")
            number_of_points = serializer.data.get("number_of_points")
            task_number = serializer.data.get("task_number")

            try:
                order_details = OrderDetail.objects.get(id=order_details)
            except OrderDetail.DoesNotExist:
                return Response(
                    {"error": "Order Don't exists with this id."}, status=404
                )

            limits = (
                20
                if order_details.number_of_points == "points_20"
                else 10
                if order_details.number_of_points == "points_10"
                else 5
            )

            essay_question = EssayQuestion.objects.filter(
                project=order_details.project, main_task_number=task_number
            ).order_by("sub_task_number")[:limits]

            task_name = order_details.project.task_instructions_question_projects.filter(
                main_task_number="task_4").first()

            serializer = EvaluationEssayQuestionSerializer(
                essay_question,
                many=True,
                context={"order_details": order_details, "task_number": task_number},
            )

            # Use the serializer in the pagination
            paginator = EssayEvaluationQuestionPagination()
            paginated_queryset = paginator.paginate_queryset(
                serializer.data, request, order_details
            )

            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="get-task-4-evaluation-question",
    )
    def get_task_4_evaluation_question_question(self, request, *args, **kwargs):
        # this help to get data of task_2, task_5,task_6,task_7 and task_8 for more information view serializer
        serializer = Task4EvaluationQuestionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order_details = serializer.data.get("order_details")

            try:
                order_details = OrderDetail.objects.get(id=order_details)
            except OrderDetail.DoesNotExist:
                return Response(
                    {"error": "Order Don't exists with this id."}, status=404
                )

            if order_details.number_of_points == "points_05":
                raise ValidationError(_("Discount has reached its total usage limit ."))

            upload_question_answers = UploadPhotoQuestion.objects.filter(
                project=order_details.project, main_task_number="task_4"
            )
            short_question_answers = ShortAnswerQuestion.objects.filter(
                project=order_details.project, main_task_number="task_4"
            )
            essay_question_answers = EssayQuestion.objects.filter(
                project=order_details.project, main_task_number="task_4"
            )

            context_data = {"order_details": order_details.id, "task_number": "task_4"}

            task_name = order_details.project.task_instructions_question_projects.filter(
                main_task_number="task_4").first()

            response_data = {
                "student_name": order_details.order.user.fullname,
                "project_name": order_details.project.title,
                "project_type": order_details.project.type.name if order_details.project.type else None,
                "task_number": "task_4",
                "task_number_evaluation": "task4",
                "task_name": task_name.task_instructions if task_name else None,
                "upload_photo_question": EvaluationUploadPhotoQuestionSerializer(
                    upload_question_answers, many=True, context=context_data
                ).data,
                "short_answer_question": EvaluationShortAnswerQuestionSerializer(
                    short_question_answers, many=True, context=context_data
                ).data,
                "essay_question_answers": EvaluationEssayQuestionSerializer(
                    essay_question_answers, many=True, context={"order_details": order_details, "task_number": "task_4"}
                ).data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="get-task-9-evaluation-question",
    )
    def get_task_9_evaluation_question_question(self, request, *args, **kwargs):
        serializer = Task4EvaluationQuestionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order_details = serializer.data.get("order_details")

            try:
                order_details = OrderDetail.objects.get(id=order_details)
            except OrderDetail.DoesNotExist:
                return Response(
                    {"error": "Order Don't exists with this id."}, status=404
                )

            if order_details.number_of_points != "points_20":
                return Response(
                    {
                        "error": "Not applicable for this order; only a 20-point project will be allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            context_data = {"order_details": order_details.id, "task_number": "task_9"}

            short_question_answers = ShortAnswerQuestion.objects.filter(
                project=order_details.project,
                main_task_number="task_9", sub_task_number=1

            )
            dropdown_question_answers = DropdownQuestion.objects.filter(
                project=order_details.project, main_task_number="task_9"
            )
            numeric_question_answers = NumericQuestion.objects.filter(
                project=order_details.project, main_task_number="task_9"
            )
            percentage_question_answers = PercentageQuestion.objects.filter(
                project=order_details.project, main_task_number="task_9"
            )

            # Step 1: Create an instance of DynamicSerializer by calling create_dynamic_serializer
            DynamicSerializer = create_dynamic_serializer(ShortAnswerQuestion)

            short_question_evaluation_serializer = DynamicSerializer(
                short_question_answers, many=True, context=context_data
            )

            DynamicSerializer = create_dynamic_serializer(DropdownQuestion)

            dropdown_question_evaluation_serializer = DynamicSerializer(
                dropdown_question_answers, many=True, context=context_data
            )

            DynamicSerializer = create_dynamic_serializer(NumericQuestion)

            numeric_question_evaluation_serializer = DynamicSerializer(
                numeric_question_answers, many=True, context=context_data
            )

            DynamicSerializer = create_dynamic_serializer(PercentageQuestion)

            percentage_question_evaluation_serializer = DynamicSerializer(
                percentage_question_answers, many=True, context=context_data
            )

            task_name = order_details.project.task_instructions_question_projects.filter(
                main_task_number="task_9").first()

            response_data = {
                "student_name": order_details.order.user.fullname,
                "student_status_id": order_details.student_task_status_order_details.id
                if order_details.student_task_status_order_details
                else None,
                "project_name": order_details.project.title,
                "project_type": order_details.project.type.name if order_details.project.type else None,
                "task_number": "task_9",
                "task_number_evaluation": "task9",
                "task_name": task_name.task_instructions if task_name else None,
                "short_answer_question": short_question_evaluation_serializer.data,
                # "dropdown_question_answers": dropdown_question_evaluation_serializer.data,
                # "numeric_question_answers": numeric_question_evaluation_serializer.data,
                # "percentage_question_answers": percentage_question_evaluation_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

    # ---------------------below api for accept or reject task question ---------------------------
    @transaction.atomic
    @action(
        methods=["post"],
        detail=False,
        url_path="evaluation-question-answers",
        url_name="evaluation_essay_question_answers",
    )
    def evaluation_question_answers(self, request, *args, **kwargs):
        serializer = EvaluationQuestionAnswersSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            essay_question_answers = serializer.data["question_answers"]
            status_of_answers = serializer.data["status"]
            get_request_model = serializer.data["model_name"]
            reject_reason = serializer.data.get("reject_reason")

            MODEL_NAMES = {
                "essay_question": "EssayQuestionAnswers",
                "upload_photo_question": "UploadPhotoQuestionAnswers",
                "short_question": "ShortQuestionAnswers",
                "numeric_question": "NumericQuestionAnswers",
                "dropdown_question": "DropDownQuestionAnswers",
                "percentage_question": "PercentageQuestionAnswers",
                "mcq_question": "MCQQuestionAnswers",
            }

            current_model_name = MODEL_NAMES.get(get_request_model)

            if current_model_name:
                current_model = apps.get_model(
                    app_label="student_project", model_name=current_model_name
                )

            try:
                obj = current_model.objects.get(id=essay_question_answers)
            except current_model.DoesNotExist:
                get_request_model = get_request_model.replace("_", " ")
                return Response(
                    {"error": f"{get_request_model} Don't exists with this id."},
                    status=404,
                )

            obj.status = status_of_answers
            if status_of_answers == "Rejected":
                obj.reject_reason = reject_reason if reject_reason else ""
            obj.save()

            return Response(
                {"success": "task status updated"}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

    # -------------this api for update student answer----------------------
    @transaction.atomic
    @action(
        methods=["post"],
        detail=False,
        url_path="edit-evaluation-answers",
        url_name="edit_evaluation_answers",
    )
    def edit_evaluation_answers(self, request, *args, **kwargs):
        serializer = EditEvaluationAnswersSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            essay_question_answers = serializer.data["question_answers"]
            get_request_model = serializer.data["model_name"]
            answer = serializer.data.get("answer")

            MODEL_NAMES = {
                "essay_question": "EssayQuestionAnswers",
                "upload_photo_question": "UploadPhotoQuestionAnswers",
                "short_question": "ShortQuestionAnswers",
                "numeric_question": "NumericQuestionAnswers",
                "dropdown_question": "DropDownQuestionAnswers",
                "percentage_question": "PercentageQuestionAnswers",
                "mcq_question": "MCQQuestionAnswers",
            }

            current_model_name = MODEL_NAMES.get(get_request_model)

            if current_model_name:
                current_model = apps.get_model(
                    app_label="student_project", model_name=current_model_name
                )

            try:
                obj = current_model.objects.get(id=essay_question_answers)
            except current_model.DoesNotExist:
                get_request_model = get_request_model.replace("_", " ")
                return Response(
                    {"error": f"{get_request_model} Don't exists with this id."},
                    status=404,
                )

            obj.answer = answer
            obj.save()

            return Response(
                {"success": "task status updated"}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )


# ----------------------below api for student evaluation status api----------------------
class StudentEvaluationStatusViewSet(APIView):
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]

    def get(self, request, order_details):
        try:
            order = OrderDetail.objects.get(id=order_details)
        except OrderDetail.DoesNotExist:
            return Response(
                {"error": "Activity Don't exists with this id."}, status=404
            )
        serializer = EvaluationResultSerializer(order, many=False).data
        serializer['task_status_id'] = order.student_task_status_order_details.id

        return Response(serializer, status=status.HTTP_200_OK)


class GetTaks03ViewSet(APIView):
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]

    def get(self, request):
        order_details_id = request.query_params.get("order_details_id")

        # Check if the parameters are provided and are valid
        if order_details_id is None:
            return Response({"error": "order_details_id is required."}, status=400)

        try:
            order_details_id = int(order_details_id)
        except ValueError:
            return Response({"error": "order_details_id must be integers."}, status=400)

        upload_photo_data = UploadPhotoQuestionAnswersSerializer(
            UploadPhotoQuestionAnswers.objects.filter(
                Q(status="Submitted") | Q(status="Accepted"),
                order_details_id=order_details_id,
                question__main_task_number="task_3"),
            many=True,
        ).data
        short_question_data = ShortQuestionAnswersSerializer(
            ShortQuestionAnswers.objects.filter(
                Q(status="Submitted") | Q(status="Accepted"),
                order_details_id=order_details_id, question__main_task_number="task_3",
            ),
            many=True,
        ).data

        numeric_question_data = NumericQuestionAnswersSerializer(
            NumericQuestionAnswers.objects.filter(
                Q(status="Submitted") | Q(status="Accepted"),
                order_details_id=order_details_id, question__main_task_number="task_3",
            ),
            many=True,
        ).data

        mcq_question_queryset = MCQQuestionAnswers.objects.filter(
            Q(status="Submitted") | Q(status="Accepted"),
            order_details_id=order_details_id, question__main_task_number="task_3",
        )

        if not mcq_question_queryset.exists():
            raise ValidationError(
                _("Invalid ID. Please provide a valid ID for this operation.")
            )

        mca_question_data = {
            "status": mcq_question_queryset.filter(question__sub_task_number=4)[
                0
            ].status
        }

        # This first loop for add response in mcq data with dynamic variable name
        for i in range(4, 21):
            key = f"mcq_question_{i}"  # set dynamic key name
            mcq_ans_sub_question = mcq_question_queryset.filter(
                question__sub_task_number=i
            )  # get data with sub-task number
            main_mcq_question = (
                mcq_ans_sub_question[0].question
                if mcq_ans_sub_question[0].question
                else None
            )  # get main question
            mca_question_data[key] = {}  # add dynamic key in mcq list
            mca_question_data[key].update(
                {f"question_{i}": main_mcq_question.question}
            )  # add question in dict

            for index, i in enumerate(
                    main_mcq_question.mca_question_option.all(), start=1
            ):  # this loop for add nested data in mcq question
                if "options" in mca_question_data[key] and isinstance(
                        mca_question_data[key]["options"], list
                ):
                    mca_question_data[key]["options"].append(i.option)
                else:
                    mca_question_data[key]["options"] = [i.option]

                if "values" in mca_question_data[key] and isinstance(
                        mca_question_data[key]["values"], list
                ):
                    mca_question_data[key]["values"].append(
                        mcq_question_queryset.filter(answer=i).count()
                    )
                else:
                    mca_question_data[key]["values"] = [
                        mcq_question_queryset.filter(answer=i).count()
                    ]

        # nested_dict = {f"option{index}": mcq_question_queryset.filter(answer=i).count(),
        #                f"option_{index}": i.option}  # add option and count
        # mca_question_data[key].update(nested_dict)  # add dynamic key in mcq question

        try:
            order_details = OrderDetail.objects.get(id=order_details_id)
        except OrderDetail.DoesNotExist:
            return Response(
                {"error": "Order Don't exists with this id."}, status=404
            )
        task_name = order_details.project.task_instructions_question_projects.filter(main_task_number="task_4").first()

        response_data = {
            "student_name": order_details.order.user.fullname,
            "project_name": order_details.project.title,
            "project_type": order_details.project.type.name if order_details.project.type else None,
            "task_number": "task_3",
            "project_id": order_details.project.id,
            "task_name": task_name.task_instructions if task_name else None,
            "order_details_id": order_details_id,
            "mca_question_data": mca_question_data,
            "uploadPhoto_question_answers": upload_photo_data,
            "short_question_answers": short_question_data,
            "numeric_question_answers": numeric_question_data,
            "student_status_id": order_details.student_task_status_order_details.id
        }

        return Response(response_data, status=status.HTTP_200_OK)


class Task3StatusViewSet(viewsets.GenericViewSet):
    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="photo-question",
        url_name="photo-question",
    )
    def photo_question(self, request, *args, **kwargs):
        serializer = Task3PhotoQuestionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order_details_id = serializer.data["order_details_id"]
            status_of_answers = serializer.data["status"]
            survey_number = serializer.data["survey_number"]
            try:
                obj = UploadPhotoQuestionAnswers.objects.get(order_details=order_details_id,
                                                             question__main_task_number="task_3",
                                                             survey_number=survey_number, status="Submitted", )
                obj.status = status_of_answers
                obj.save()
            except UploadPhotoQuestionAnswers.DoesNotExist:
                return Response(
                    {"error": "Upload Photo Question Don't exists with this id."},
                    status=404,
                )
            if status_of_answers == "Accepted":
                try:
                    obj = ShortQuestionAnswers.objects.get(
                        order_details=order_details_id,
                        question__main_task_number="task_3",
                        survey_number=survey_number,
                        status="Submitted",
                    )
                    obj.status = status_of_answers
                    obj.save()
                except ShortQuestionAnswers.DoesNotExist:
                    pass
                    # return Response(
                    #     {"error": "Short Question Don't exists with this id."}, status=404
                    # )

                try:
                    obj = NumericQuestionAnswers.objects.get(
                        order_details=order_details_id,
                        survey_number=survey_number,
                        question__main_task_number="task_3",
                        status="Submitted",
                    )
                    obj.status = status_of_answers
                    obj.save()
                except NumericQuestionAnswers.DoesNotExist:
                    pass
                    # return Response(
                    #     {"error": "Numeric Question Don't exists with this id."}, status=404
                    # )

            # try:
            #     if status_of_answers == "Rejected":
            #         obj = StudentTaskStatus.objects.get(order_details=order_details_id,)
            #         obj.status = status_of_answers
            #         obj.save()
            # except StudentTaskStatus.DoesNotExist:
            #     return Response(
            #         {"error": "Student Task Status Don't exists with this id."},
            #         status=404,
            #     )

            return Response(
                {"success": "task status updated"}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

    @transaction.atomic
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="mcq-question",
        url_name="mcq-question",
    )
    def mcq_question(self, request, *args, **kwargs):
        serializer = Task3McqQuestionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order_details_id = serializer.data["order_details_id"]
            status_of_answers = serializer.data["status"]
            if status_of_answers == "Rejected":
                try:
                    obj = UploadPhotoQuestionAnswers.objects.filter(
                        order_details=order_details_id,
                        question__main_task_number="task_3",
                    )
                    obj.update(status=status_of_answers)
                except UploadPhotoQuestionAnswers.DoesNotExist:
                    return Response(
                        {"error": "Upload Photo Question Don't exists with this id."},
                        status=404,
                    )

                try:
                    obj = ShortQuestionAnswers.objects.filter(
                        order_details=order_details_id,
                        question__main_task_number="task_3",
                    )
                    obj.update(status=status_of_answers)
                except ShortQuestionAnswers.DoesNotExist:
                    return Response(
                        {"error": "Short Question Don't exists with this id."},
                        status=404,
                    )

                try:
                    obj = NumericQuestionAnswers.objects.filter(
                        order_details=order_details_id,
                        question__main_task_number="task_3",
                    )
                    obj.update(status=status_of_answers)
                except NumericQuestionAnswers.DoesNotExist:
                    return Response(
                        {"error": "Numeric Question Don't exists with this id."},
                        status=404,
                    )

                try:
                    obj = MCQQuestionAnswers.objects.filter(
                        order_details=order_details_id,
                        question__main_task_number="task_3",
                    )
                    obj.update(status=status_of_answers)
                except MCQQuestionAnswers.DoesNotExist:
                    return Response(
                        {"error": "Student Task Status Don't exists with this id."},
                        status=404,
                    )

                try:
                    obj = StudentTaskStatus.objects.get(
                        order_details=order_details_id,
                    )
                    obj.task3 = "answer_rejected_in_evaluation"
                    obj.task3_submissions = 0
                    obj.save()
                except StudentTaskStatus.DoesNotExist:
                    return Response(
                        {"error": "Student Task Status Don't exists with this id."},
                        status=404,
                    )
            else:
                try:
                    obj = MCQQuestionAnswers.objects.filter(
                        order_details=order_details_id, status="Submitted", question__main_task_number="task_3",
                    )
                    obj.update(status=status_of_answers)
                except MCQQuestionAnswers.DoesNotExist:
                    return Response(
                        {"error": "Student Task Status Don't exists with this id."},
                        status=404,
                    )

            return Response(
                {"success": "task status updated"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )
