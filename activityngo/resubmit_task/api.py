from django.apps import apps
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from activityngo.resubmit_task.render import DynamicRejectedQuestionRenderer
from activityngo.resubmit_task.serializers import (
    DynamicRejectedQuestionSerializer, dynamic_question_answer_serializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class ResubmitTaskViewSet(viewsets.GenericViewSet):
    renderer_classes = [DynamicRejectedQuestionRenderer]

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
        url_path="get-dynamic-rejected-question",
        url_name="get-dynamic-rejected-question",
    )
    def get_dynamic_rejected_question(self, request, *args, **kwargs):
        serializer = DynamicRejectedQuestionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reject_data = serializer.data["reject_data"]

            MODEL_NAMES = {
                "essay_question": "EssayQuestionAnswers",
                "upload_photo_question": "UploadPhotoQuestionAnswers",
                "short_question": "ShortQuestionAnswers",
                "numeric_question": "NumericQuestionAnswers",
                "dropdown_question": "DropDownQuestionAnswers",
                "percentage_question": "PercentageQuestionAnswers",
                "mcq_question": "MCQQuestionAnswers",
                "exit_question": "ExitQuestionAnswers",
            }
            response_data = []
            for current_model_name in reject_data:
                model_name = MODEL_NAMES.get(current_model_name.get("model_name"))

                if not model_name:
                    return Response(
                        {"error": "Invalid model name."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                model_name = apps.get_model(
                    app_label="student_project", model_name=model_name
                )

                try:
                    obj = model_name.objects.get(
                        id=current_model_name.get("question_id")
                    )
                except model_name.DoesNotExist:
                    get_request_model = current_model_name.get("model_name").replace(
                        "_", " "
                    )
                    return Response(
                        {"error": f"{get_request_model} Don't exists with this id."},
                        status=404,
                    )

                DynamicSerializer = dynamic_question_answer_serializer(model_name)
                data = DynamicSerializer(obj, many=False)

                response_data.append(data.data)
            return Response({"results": response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

    # @action(
    #     detail=False,
    #     methods=["POST"],
    #     permission_classes=[IsAPIKEYAuthenticated, IsAuthenticated],
    #     url_path="get-task-3-dynamic-rejected-question",
    #     url_name="get-task-3-dynamic-rejected-question",
    # )
    # def get_task_3_dynamic_rejected_question(self, request, *args, **kwargs):
    #     serializer = DynamicTask3RejectedQuestionSerializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     survey_person_data = []
    #     for i in upload_reject_question_final_count:
    #         name_obj = obj.short_question_order_details.filter(question__main_task_number="task_3",
    #                                                            survey_number=i.survey_number).order_by(
    #             '-create_time').first()
    #         age_obj = obj.numeric_question_order_details.filter(question__main_task_number="task_3",
    #                                                             survey_number=i.survey_number).order_by(
    #             '-create_time').first()
    #
    #
    #
    #
    #         name = name_obj.answer if name_obj else None
    #         age = age_obj.answer if age_obj else None
    #         image = i.answer
    #
    #         data = {
    #             "name": name,
    #             "age": age,
    #             "image": image.url if image else None
    #         }
    #
    #         survey_person_data.append(data)