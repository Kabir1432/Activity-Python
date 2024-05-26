from rest_framework import serializers
from django.db.models import Max, Subquery, OuterRef
from activityngo.order.models import OrderDetail
from activityngo.project.models import Project
from activityngo.question_types.models import (
    EssayQuestion,
    ShortAnswerQuestion,
    UploadPhotoQuestion,
)
from activityngo.question_types.serializers import (
    DropdownQuestionSerializer,
    NumericQuestionSerializer,
    ShortAnswerQuestionSerializer,
    TaskInstructionsListSerializer,
    UploadPhotoQuestionSerializer,
)
from activityngo.student_project.models import (
    DropDownQuestionAnswers,
    EssayQuestionAnswers,
    NumericQuestionAnswers,
    ShortQuestionAnswers,
    StudentTaskStatus,
    UploadPhotoQuestionAnswers,
)
from activityngo.student_project.serializer import StudentTaskStatusSerializer


class EvaluationProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    task_02 = serializers.SerializerMethodField()
    task_03 = serializers.SerializerMethodField()
    task_04 = serializers.SerializerMethodField()
    task_05 = serializers.SerializerMethodField()
    task_06 = serializers.SerializerMethodField()
    task_07 = serializers.SerializerMethodField()
    task_08 = serializers.SerializerMethodField()
    task_09 = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "category",
            "category_name",
            "subscription_price",
            "gst_inclusive",
            "price_of_20_point",
            "task_02",
            "task_03",
            "task_04",
            "task_05",
            "task_06",
            "task_07",
            "task_08",
            "task_09",
        ]

    def get_category_name(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_02(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_03(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_04(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_05(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_06(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_07(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_08(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_09(self, obj):
        try:
            return obj.category.name
        except:
            return ""


class EvaluationFor05PointProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    task_02 = serializers.SerializerMethodField()
    task_03 = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "category",
            "category_name",
            "subscription_price",
            "gst_inclusive",
            "price_of_20_point",
            "task_02",
            "task_03",
        ]

    def get_category_name(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_02(self, obj):
        try:
            task_2_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task2="submitted_for_evaluation",
                order_details__number_of_points="points_05",
            ).count()
            return task_2_complete_count
        except:
            return ""

    def get_task_03(self, obj):
        try:
            task_3_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task3="submitted_for_evaluation",
                order_details__number_of_points="points_05",
            ).count()
            return task_3_complete_count
        except:
            return ""


class EvaluationFor10PointProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    task_02 = serializers.SerializerMethodField()
    task_03 = serializers.SerializerMethodField()
    task_04 = serializers.SerializerMethodField()
    task_05 = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "category",
            "category_name",
            "subscription_price",
            "gst_inclusive",
            "price_of_20_point",
            "task_02",
            "task_03",
            "task_04",
            "task_05",
        ]

    def get_category_name(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_02(self, obj):
        try:
            task_2_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task2="submitted_for_evaluation",
                order_details__number_of_points="points_10",
            ).count()
            return task_2_complete_count
        except:
            return ""

    def get_task_03(self, obj):
        try:
            task_3_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task3="submitted_for_evaluation",
                order_details__number_of_points="points_10",
            ).count()
            return task_3_complete_count
        except:
            return ""

    def get_task_04(self, obj):
        try:
            task_4_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task4="submitted_for_evaluation",
                order_details__number_of_points="points_10",
            ).count()
            return task_4_complete_count
        except:
            return ""

    def get_task_05(self, obj):
        try:
            task_5_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task5="submitted_for_evaluation",
            ).count()
            return task_5_complete_count
        except:
            return ""


class EvaluationFor20PointProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    task_02 = serializers.SerializerMethodField()
    task_03 = serializers.SerializerMethodField()
    task_04 = serializers.SerializerMethodField()
    task_05 = serializers.SerializerMethodField()
    task_06 = serializers.SerializerMethodField()
    task_07 = serializers.SerializerMethodField()
    task_08 = serializers.SerializerMethodField()
    task_09 = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "category",
            "category_name",
            "subscription_price",
            "gst_inclusive",
            "price_of_20_point",
            "task_02",
            "task_03",
            "task_04",
            "task_05",
            "task_06",
            "task_07",
            "task_08",
            "task_09",
        ]

    def get_category_name(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_task_02(self, obj):
        try:
            task_2_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task2="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_2_complete_count
        except:
            return ""

    def get_task_03(self, obj):
        try:
            task_3_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task3="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_3_complete_count
        except:
            return ""

    def get_task_04(self, obj):
        try:
            task_4_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task4="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_4_complete_count
        except:
            return ""

    def get_task_05(self, obj):
        try:
            task_5_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task5="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_5_complete_count
        except:
            return ""

    def get_task_06(self, obj):
        try:
            task_6_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task6="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_6_complete_count
        except:
            return ""

    def get_task_07(self, obj):
        try:
            task_7_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task7="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_7_complete_count
        except:
            return ""

    def get_task_08(self, obj):
        try:
            task_8_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task8="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_8_complete_count
        except:
            return ""

    def get_task_09(self, obj):
        try:
            task_9_complete_count = StudentTaskStatus.objects.filter(
                order_details__project=obj,
                order_details__is_expire=False,
                task9="submitted_for_evaluation",
                order_details__number_of_points="points_20",
            ).count()
            return task_9_complete_count
        except:
            return ""


class OrderDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    evaluation_status = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = (
            "id",
            "customer_name",
            "evaluation_status",
        )  # Include any other fields you need

    def get_evaluation_status(self, obj):
        try:
            queryset = StudentTaskStatus.objects.filter(
                order_details=obj,
            ).first()
            data = StudentTaskStatusSerializer(queryset, many=False).data

            return data
        except:
            return ""

    def get_customer_name(self, obj):
        try:
            return obj.order.user.fullname
        except:
            return ""


class EssayQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayQuestion
        fields = (
            "id",
            "project",
            "main_task_number",
            "sub_task_number",
            "question",
            "answer",
            "question_character_maximum_limit",
            "copy_paste_question_box",
            "special_characters_in_questions",
            "action_needed",
            "characters_allowed_in_answer_box",
            "special_characters_in_answer_box",
            "grammar_check_in_answer_box",
            "answer_character_minimum_limit",
            "answer_character_maximum_limit",
        )


class EssayQuestionAnswersSerializer(serializers.ModelSerializer):
    question = EssayQuestionSerializer(
        read_only=True,
    )

    class Meta:
        model = EssayQuestionAnswers
        fields = (
            "id",
            "question",
            "user",
            "status",
            "answer",
            "order_details",
            "survey_number",
        )


class EvaluationEssayQuestionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = EssayQuestion
        fields = (
            "id",
            "project",
            "main_task_number",
            "sub_task_number",
            "question",
            "status",
        )

    def get_status(self, obj):
        try:
            order_details = self.context.get("order_details")
            task_number = self.context.get("task_number")
            status_obj = obj.essay_question_answers.filter(
                order_details=order_details, question__main_task_number=task_number
            )
            status = {
                "question_type": "essay_question",
                "student_status_id": order_details.student_task_status_order_details.id
                if order_details.student_task_status_order_details
                else None,
                "number_of_time_reject": status_obj.filter(
                    status="Rejected"
                ).count(),
            }

            if status_obj.filter(status="Accepted").exists():
                status.update(
                    {
                        "status": "Accepted",
                        "answer": status_obj.filter(status="Accepted")[0].answer,
                    }
                )
            elif status_obj.filter(status="Submitted").exists():
                status.update(
                    {
                        "id": status_obj.filter(status="Submitted")[0].id,
                        "status": "Submitted",
                        "answer": status_obj.filter(status="Submitted")[0].answer,
                    }
                )
            elif status_obj.filter(status="Rejected").exists():
                status.update(
                    {
                        "status": "Rejected",
                        "answer": status_obj.filter(status="Rejected")
                        .order_by("-create_time")[0]
                        .answer,

                    }
                )
            else:
                status.update({"status": "Status not found"})

            return status
        except Exception as e:
            return ""


class EvaluationShortAnswerQuestionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = ShortAnswerQuestion
        fields = (
            "id",
            "project",
            "main_task_number",
            "sub_task_number",
            "question",
            "status",
        )

    def get_status(self, obj):
        try:
            order_details = self.context.get("order_details")
            task_number = self.context.get("task_number")
            status_obj = obj.short_question_answers.filter(
                order_details=order_details, question__main_task_number=task_number
            )
            order_details = OrderDetail.objects.get(pk=order_details)
            status = {
                "question_type": "short_question",
                "student_status_id": order_details.student_task_status_order_details.id
                if order_details.student_task_status_order_details
                else None,
                "number_of_time_reject": status_obj.filter(
                    status="Rejected"
                ).count(),
            }

            if status_obj.filter(status="Accepted").exists():
                status.update(
                    {
                        "status": "Accepted",
                        "answer": status_obj.filter(status="Accepted")[0].answer,
                    }
                )
            elif status_obj.filter(status="Submitted").exists():
                status.update(
                    {
                        "id": status_obj.filter(status="Submitted")[0].id,
                        "status": "Submitted",
                        "answer": status_obj.filter(status="Submitted")[0].answer,
                    }
                )
            elif status_obj.filter(status="Rejected").exists():
                status.update(
                    {
                        "status": "Rejected",
                        "answer": status_obj.filter(status="Rejected")
                        .order_by("-create_time")[0]
                        .answer,

                    }
                )
            else:
                status.update({"status": "Status not found"})

            return status
        except Exception as e:
            print(e)
            return ""


class EvaluationUploadPhotoQuestionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = UploadPhotoQuestion
        fields = (
            "id",
            "project",
            "main_task_number",
            "sub_task_number",
            "question",
            "status",
        )

    def get_status(self, obj):
        try:
            order_details = self.context.get("order_details")
            status_obj = obj.upload_photo_question_answers.filter(
                order_details=order_details, question__main_task_number="task_4"
            )
            order_details = OrderDetail.objects.get(pk=order_details)
            status = {
                "question_type": "upload_photo_question",
                "student_status_id": order_details.student_task_status_order_details.id
                if order_details.student_task_status_order_details
                else None,
                "number_of_time_reject": status_obj.filter(
                    status="Rejected"
                ).count(),
            }

            if status_obj.filter(status="Accepted").exists():
                status.update(
                    {
                        "status": "Accepted",
                        "answer": status_obj.filter(status="Accepted")[0].answer.url,
                    }
                )
            elif status_obj.filter(status="Submitted").exists():
                status.update(
                    {
                        "id": status_obj.filter(status="Submitted")[0].id,
                        "status": "Submitted",
                        "answer": status_obj.filter(status="Submitted")[0].answer.url,
                    }
                )
            elif status_obj.filter(status="Rejected").exists():
                status.update(
                    {
                        "status": "Rejected",
                        "answer": status_obj.filter(status="Rejected")
                        .order_by("-create_time")[0]
                        .answer.url,

                    }
                )
            else:
                status.update({"status": "Status not found"})
            return status
        except Exception as e:
            print(e)
            return ""


class UploadPhotoQuestionAnswersSerializer(serializers.ModelSerializer):
    question = UploadPhotoQuestionSerializer(
        read_only=True,
    )

    class Meta:
        model = UploadPhotoQuestionAnswers
        fields = (
            "id",
            "question",
            "user",
            "status",
            "answer",
            "order_details",
            "survey_number",
        )


class ShortQuestionAnswersSerializer(serializers.ModelSerializer):
    question = ShortAnswerQuestionSerializer(
        read_only=True,
    )

    class Meta:
        model = ShortQuestionAnswers
        fields = (
            "id",
            "question",
            "user",
            "status",
            "answer",
            "order_details",
            "survey_number",
        )


# class EvaluationDropdownQuestionSerializer(serializers.ModelSerializer):
#     status = serializers.SerializerMethodField()
#
#     class Meta:
#         model = DropdownQuestion
#         fields = ('id', 'project', 'main_task_number', 'sub_task_number', 'question', 'status')
#
#     def get_status(self, obj):
#         try:
#             order_details = self.context.get('order_details')
#             status_obj = obj.dropdown_question_answers.filter(order_details=order_details,
#                                                               question__main_task_number="task_4")
#             status = {"question_type": "dropdown_question", }
#
#             if status_obj.filter(status="Accepted").exists():
#                 status.update({"status": "Accepted"})
#             elif status_obj.filter(status="Submitted").exists():
#                 import pdb
#                 pdb.set_trace()
#                 status.update({"id": status_obj.filter(status="Submitted")[0].id, "status": "Submitted",
#                                "answer": status_obj.filter(status="Submitted")[0].answer})
#             elif status_obj.filter(status="Rejected").exists():
#                 status.update(
#                     {"status": "Rejected", "number_of_time_reject": status_obj.filter(status="Rejected").count()})
#             else:
#                 status.update({"status": "Status not found"})
#             return status
#         except:
#             return ""
#
#
# class EvaluationNumericQuestionSerializer(serializers.ModelSerializer):
#     status = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ShortAnswerQuestion
#         fields = ('id', 'project', 'main_task_number', 'sub_task_number', 'question', 'status')
#
#     def get_status(self, obj):
#         try:
#             order_details = self.context.get('order_details')
#             task_number = self.context.get('task_number')
#             status_obj = obj.essay_question_answers.filter(order_details=order_details,
#                                                            question__main_task_number=task_number)
#             status = {"question_type": "essay_question", }
#
#             if status_obj.filter(status="Accepted").exists():
#                 status.update({"status": "Accepted"})
#             elif status_obj.filter(status="Submitted").exists():
#                 status.update({"id": status_obj.filter(status="Submitted")[0].id, "status": "Submitted",
#                                "answer": status_obj.filter(status="Submitted")[0].answer})
#             elif status_obj.filter(status="Rejected").exists():
#                 status.update(
#                     {"status": "Rejected", "number_of_time_reject": status_obj.filter(status="Rejected").count()})
#             else:
#                 status.update({"status": "Status not found"})
#
#             return status
#         except:
#             return ""


def create_dynamic_serializer(model_name):
    # Define a serializer class dynamically
    class DynamicSerializer(serializers.ModelSerializer):
        status = serializers.SerializerMethodField()

        class Meta:
            model = model_name  # Set the model dynamically
            fields = (
                "id",
                "project",
                "main_task_number",
                "sub_task_number",
                "question",
                "status",
            )

        def get_status(self, obj):
            try:
                order_details = self.context.get("order_details")
                current_model_name = obj._meta.model.__name__
                model_related_name = {
                    "ShortAnswerQuestion": "short_question_answers",
                    "DropdownQuestion": "dropdown_question_answers",
                    "NumericQuestion": "numeric_question_answers",
                    "PercentageQuestion": "percentage_question_answers",
                }
                status_obj = getattr(
                    obj, model_related_name.get(current_model_name)
                ).filter(
                    order_details=order_details, question__main_task_number="task_9"
                )
                response_model_name = {
                    "ShortAnswerQuestion": "short_question",
                    "DropdownQuestion": "dropdown_question",
                    "NumericQuestion": "numeric_question",
                    "PercentageQuestion": "percentage_question",
                }
                status = {
                    "question_type": response_model_name.get(current_model_name),
                    "number_of_time_reject": status_obj.filter(
                        status="Rejected"
                    ).count(),
                }
                if status_obj.filter(status="Accepted").exists():
                    if current_model_name != "DropdownQuestion":
                        answer = status_obj.filter(status="Accepted")[0].answer
                    else:
                        answer = status_obj.filter(status="Accepted")[0].answer.option
                    status.update(
                        {
                            "status": "Accepted",
                            "answer": answer,

                        }
                    )
                elif status_obj.filter(status="Submitted").exists():
                    if current_model_name != "DropdownQuestion":
                        answer = status_obj.filter(status="Submitted")[0].answer
                    else:
                        answer = status_obj.filter(status="Submitted")[0].answer.option
                    status.update(
                        {
                            "id": status_obj.filter(status="Submitted")[0].id,
                            "status": "Submitted",
                            "answer": answer,
                        }
                    )
                elif status_obj.filter(status="Rejected").exists():
                    if current_model_name != "DropdownQuestion":
                        answer = (
                            status_obj.filter(status="Rejected")
                            .order_by("-create_time")[0]
                            .answer
                        )
                    else:
                        answer = (
                            status_obj.filter(status="Rejected")
                            .order_by("-create_time")[0]
                            .answer.option
                        )
                    status.update(
                        {
                            "status": "Rejected",
                            "answer": answer,

                        }
                    )
                else:
                    status.update({"status": "Status not found"})
                return status
            except Exception as e:
                return "error"

    return DynamicSerializer


class DropDownQuestionAnswersSerializer(serializers.ModelSerializer):
    question = DropdownQuestionSerializer(
        read_only=True,
    )

    class Meta:
        model = DropDownQuestionAnswers
        fields = (
            "id",
            "question",
            "user",
            "status",
            "answer",
            "order_details",
            "survey_number",
        )


class NumericQuestionAnswersSerializer(serializers.ModelSerializer):
    question = NumericQuestionSerializer(
        read_only=True,
    )

    class Meta:
        model = NumericQuestionAnswers
        fields = (
            "id",
            "question",
            "user",
            "status",
            "answer",
            "order_details",
            "survey_number",
        )


class EvaluationResultSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()

    task_1_instruction = serializers.SerializerMethodField()
    task_2_instruction = serializers.SerializerMethodField()
    task_3_instruction = serializers.SerializerMethodField()
    task_4_instruction = serializers.SerializerMethodField()
    task_5_instruction = serializers.SerializerMethodField()
    task_6_instruction = serializers.SerializerMethodField()
    task_7_instruction = serializers.SerializerMethodField()
    task_8_instruction = serializers.SerializerMethodField()
    task_9_instruction = serializers.SerializerMethodField()
    task_10_instruction = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = (
            "id",
            "customer_name",
            "number_of_points",
            "task_1_instruction",
            "task_2_instruction",
            "task_3_instruction",
            "task_4_instruction",
            "task_5_instruction",
            "task_6_instruction",
            "task_7_instruction",
            "task_8_instruction",
            "task_9_instruction",
            "task_10_instruction",
        )  # Include any other fields you need

    def get_customer_name(self, obj):
        try:
            return obj.order.user.fullname
        except:
            return ""

    def get_task_1_instruction(self, obj):
        data = TaskInstructionsListSerializer(
            obj.project.task_instructions_question_projects.filter(
                main_task_number="task_1"
            ).first()
        ).data
        task_status = {
            "total_questions": 2,
            "correct_answers": 2
            if obj.student_task_status_order_details.task1 == "all_answers_are_accepted"
            else 0,
            "wrong_answers": 0,
            "total_videos": "Total Videos",
            "watched_videos": "Watched Videos",
            "not_submitted": 0
            if obj.student_task_status_order_details.task1 == "all_answers_are_accepted"
            else 2,
            "submitted_for_evaluation": 0
        }
        data.update(task_status)
        return data

    def get_task_2_instruction(self, obj):
        data = TaskInstructionsListSerializer(
            obj.project.task_instructions_question_projects.filter(
                main_task_number="task_2"
            ).first()
        ).data
        accepted_ids = obj.essay_question_order_details.filter(
            status="Accepted", question__main_task_number="task_2"
        ).values_list("question", flat=True)
        submit_ids = obj.essay_question_order_details.filter(
            status="Submitted", question__main_task_number="task_2"
        ).values_list("question", flat=True)
        final_count = obj.essay_question_order_details.exclude(
            question__in=accepted_ids,
        ).filter(question__main_task_number="task_2")
        final_count = final_count.exclude(
            question__in=submit_ids,
        )

        reject_question_final_count = (
            final_count.filter(status="Rejected", question=OuterRef("question"))
            .order_by("-create_time")
            .values_list("create_time")[:1]
        )
        reject_question_final_count = final_count.filter(
            create_time=Subquery(reject_question_final_count)
        )
        total_questions = 20 if obj.number_of_points == "points_20" else 10 if obj.number_of_points == "points_10" else 5

        task_status = {
            "total_questions": total_questions,
            "correct_answers": len(accepted_ids),
            "wrong_answers": reject_question_final_count.count(),
            "wrong_answers_list": {
                "essay_question": reject_question_final_count.values_list(
                    "id", flat=True
                ).distinct(),

            },
            "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
            "submitted_for_evaluation": len(submit_ids)
        }
        data.update(task_status)
        return data

    def get_task_3_instruction(self, obj):
        if obj.student_task_status_order_details.task3 == "answer_rejected_in_evaluation":
            return {"all_survey_rejected": "All Survey's are rejected please re-do Task-3.",
                    "status": "answer_rejected_in_evaluation"}
        data = TaskInstructionsListSerializer(
            obj.project.task_instructions_question_projects.filter(
                main_task_number="task_3"
            ).first()
        ).data

        # upload_photo_question_order_details

        upload_photo_accepted_ids = obj.upload_photo_question_order_details.filter(
            status="Accepted", question__main_task_number="task_3"
        ).values_list("survey_number", flat=True)
        upload_photo_submit_ids = obj.upload_photo_question_order_details.filter(
            status="Submitted", question__main_task_number="task_3"
        ).values_list("survey_number", flat=True)
        upload_photo_final_count = obj.upload_photo_question_order_details.exclude(
            survey_number__in=upload_photo_accepted_ids,
        ).filter(question__main_task_number="task_3")
        upload_photo_final_count = upload_photo_final_count.exclude(
            survey_number__in=upload_photo_submit_ids,
        )

        upload_reject_question_final_count = (
            upload_photo_final_count.filter(
                status="Rejected", survey_number=OuterRef("survey_number")
            )
            .order_by("-create_time")
            .values_list("create_time")[:1]
        )
        upload_reject_question_final_count = upload_photo_final_count.filter(
            create_time=Subquery(upload_reject_question_final_count)
        )

        survey_person_data = [
        ]
        for i in upload_reject_question_final_count:
            name = obj.short_question_order_details.filter(question__main_task_number="task_3",
                                                           survey_number=i.survey_number).order_by(
                '-create_time').first()
            age = obj.numeric_question_order_details.filter(question__main_task_number="task_3",
                                                            survey_number=i.survey_number).order_by(
                '-create_time').first()
            image = i.answer
            person_data = {
                "id": str(i.question.id),
                "name": name.answer if name else None,
                "age": age.answer if age else None,
                "image": image.url if image else None,
                "survey_number": i.survey_number
            }
            survey_person_data.append(person_data)
        total_questions = 6 if obj.number_of_points != "points_20" else 10
        task_status = {
            "total_questions": total_questions,
            "correct_answers": len(upload_photo_accepted_ids),
            "wrong_answers": upload_reject_question_final_count.count(),

            "wrong_answers_list": {
                "upload_phot_question_id": upload_reject_question_final_count.values_list(
                    "question", flat=True
                ).distinct().first(),
                "survey_person_data": survey_person_data,
            },
            "total_surveys": "Total Surveys",
            "correct_photos": "Correct Photos",
            "rejected_photos": "Rejected Photos",
            "not_submitted": total_questions - len(upload_photo_accepted_ids) - len(upload_photo_submit_ids),
            "submitted_for_evaluation": len(upload_photo_submit_ids)
        }
        data.update(task_status)
        return data

    def get_task_4_instruction(self, obj):
        if obj.number_of_points == "points_05":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_10"
                ).first()
            ).data
            data["main_task_number"] = "task_4"
            accepted_ids = obj.exit_question_order_details.filter(
                status="Accepted"
            ).values_list("question", flat=True)
            submit_ids = obj.exit_question_order_details.filter(
                status="question"
            ).values_list("id", flat=True)
            final_count = obj.exit_question_order_details.exclude(
                question__in=accepted_ids,
            ).all()
            final_count = final_count.exclude(
                question__in=submit_ids,
            )

            reject_question_final_count = (
                final_count.filter(status="Rejected", question=OuterRef("question"))
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            reject_question_final_count = final_count.filter(
                create_time=Subquery(reject_question_final_count)
            )
            total_questions = 20
            task_status = {
                "total_questions": total_questions,
                "correct_answers": len(accepted_ids),
                "wrong_answers": reject_question_final_count.count(),
                "wrong_answers_list": {
                    "exit_question": reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct()
                },
                "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
                "submitted_for_evaluation": len(submit_ids)
            }
            data.update(task_status)
        else:
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_4"
                ).first()
            ).data

            # upload_photo_question_order_details

            upload_photo_accepted_ids = obj.upload_photo_question_order_details.filter(
                status="Accepted", question__main_task_number="task_4"
            ).values_list("question", flat=True)
            upload_photo_submit_ids = obj.upload_photo_question_order_details.filter(
                status="Submitted", question__main_task_number="task_4"
            ).values_list("question", flat=True)
            upload_photo_final_count = obj.upload_photo_question_order_details.exclude(
                question__in=upload_photo_accepted_ids,
            ).filter(question__main_task_number="task_4")
            upload_photo_final_count = upload_photo_final_count.exclude(
                question__in=upload_photo_submit_ids,
            )

            upload_reject_question_final_count = (
                upload_photo_final_count.filter(
                    status="Rejected", question=OuterRef("question")
                )
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            upload_reject_question_final_count = upload_photo_final_count.filter(
                create_time=Subquery(upload_reject_question_final_count)
            )

            # short_question_order_details

            short_question_accepted_ids = obj.short_question_order_details.filter(
                status="Accepted", question__main_task_number="task_4"
            ).values_list("question", flat=True)
            short_question_submit_ids = obj.short_question_order_details.filter(
                status="Submitted", question__main_task_number="task_4"
            ).values_list("question", flat=True)
            short_question_final_count = obj.short_question_order_details.exclude(
                question__in=short_question_accepted_ids,
            ).filter(question__main_task_number="task_4")
            short_question_final_count = short_question_final_count.exclude(
                question__in=short_question_submit_ids,
            )

            short_reject_question_final_count = (
                short_question_final_count.filter(
                    status="Rejected", question=OuterRef("question")
                )
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            short_reject_question_final_count = short_question_final_count.filter(
                create_time=Subquery(short_reject_question_final_count)
            )

            # essay_question_order_details

            essay_question_accepted_ids = obj.essay_question_order_details.filter(
                status="Accepted", question__main_task_number="task_4"
            ).values_list("question", flat=True)
            essay_question_submit_ids = obj.essay_question_order_details.filter(
                status="Submitted", question__main_task_number="task_4"
            ).values_list("question", flat=True)
            essay_question_final_count = obj.essay_question_order_details.exclude(
                question__in=essay_question_accepted_ids,
            ).filter(question__main_task_number="task_4")
            essay_question_final_count = essay_question_final_count.exclude(
                question__in=essay_question_submit_ids,
            )

            essay_reject_question_final_count = (
                essay_question_final_count.filter(
                    status="Rejected", question=OuterRef("question")
                )
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            essay_reject_question_final_count = essay_question_final_count.filter(
                create_time=Subquery(essay_reject_question_final_count)
            )
            total_questions = 13
            accepted_ids = len(upload_photo_accepted_ids) + len(short_question_accepted_ids) + len(
                essay_question_accepted_ids)
            submit_ids = len(upload_photo_submit_ids) + len(short_question_submit_ids) + len(essay_question_submit_ids)
            task_status = {
                "total_questions": total_questions,
                "correct_answers": accepted_ids,
                "wrong_answers": upload_reject_question_final_count.count()
                                 + short_reject_question_final_count.count()
                                 + essay_reject_question_final_count.count(),
                "wrong_answers_list": {
                    "upload_photo_question": upload_reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct(),
                    "short_question": short_reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct(),
                    "essay_question": essay_reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct(),

                },
                "not_submitted": total_questions - accepted_ids - submit_ids,
                "submitted_for_evaluation": submit_ids
            }
            data.update(task_status)
        return data

    def get_task_5_instruction(self, obj):
        if obj.number_of_points == "points_20" or obj.number_of_points == "points_10":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_5"
                ).first()
            ).data
            accepted_ids = obj.essay_question_order_details.filter(
                status="Accepted", question__main_task_number="task_5"
            ).values_list("question", flat=True)
            submit_ids = obj.essay_question_order_details.filter(
                status="Submitted", question__main_task_number="task_5"
            ).values_list("question", flat=True)
            final_count = obj.essay_question_order_details.exclude(
                question__in=accepted_ids,
            ).filter(question__main_task_number="task_5")
            final_count = final_count.exclude(
                question__in=submit_ids,
            )

            reject_question_final_count = (
                final_count.filter(status="Rejected", question=OuterRef("question"))
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            reject_question_final_count = final_count.filter(
                create_time=Subquery(reject_question_final_count)
            )
            total_questions = 5
            task_status = {
                "total_questions": total_questions,
                "correct_answers": len(accepted_ids),
                # "wrong_answers": final_count.filter(status="Rejected").values('question').distinct(),
                "wrong_answers": reject_question_final_count.count(),
                "wrong_answers_list": {
                    "essay_question": reject_question_final_count.values_list(
                        "id", flat=True
                    )
                },
                "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
                "submitted_for_evaluation": len(submit_ids)
            }
            data.update(task_status)
            return data
        return None

    def get_task_6_instruction(self, obj):
        if obj.number_of_points == "points_20":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_6"
                ).first()
            ).data

            # essay_question_order_details

            accepted_ids = obj.essay_question_order_details.filter(
                status="Accepted", question__main_task_number="task_6"
            ).values_list("question", flat=True)
            submit_ids = obj.essay_question_order_details.filter(
                status="Submitted", question__main_task_number="task_6"
            ).values_list("question", flat=True)
            final_count = obj.essay_question_order_details.exclude(
                question__in=accepted_ids,
            ).filter(question__main_task_number="task_6")
            final_count = final_count.exclude(
                question__in=submit_ids,
            )

            reject_question_final_count = (
                final_count.filter(status="Rejected", question=OuterRef("question"))
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            reject_question_final_count = final_count.filter(
                create_time=Subquery(reject_question_final_count)
            )
            total_questions = 5
            task_status = {
                "total_questions": total_questions,
                "correct_answers": len(accepted_ids),
                "wrong_answers": reject_question_final_count.count(),
                "wrong_answers_list": {
                    "essay_question": reject_question_final_count.values_list(
                        "id", flat=True
                    )
                },
                "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
                "submitted_for_evaluation": len(submit_ids)
            }
            data.update(task_status)
            return data
        elif obj.number_of_points == "points_10":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_10"
                ).first()
            ).data
            data["main_task_number"] = "task_6"
            accepted_ids = obj.exit_question_order_details.filter(
                status="Accepted"
            ).values_list("question", flat=True)
            submit_ids = obj.exit_question_order_details.filter(
                status="Submitted"
            ).values_list("question", flat=True)
            final_count = obj.exit_question_order_details.exclude(
                question__in=accepted_ids,
            ).all()
            final_count = final_count.exclude(
                question__in=submit_ids,
            )

            reject_question_final_count = (
                final_count.filter(status="Rejected", question=OuterRef("question"))
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            reject_question_final_count = final_count.filter(
                create_time=Subquery(reject_question_final_count)
            )
            total_questions = 20
            task_status = {
                "total_questions": total_questions,
                "correct_answers": len(accepted_ids),
                "wrong_answers": reject_question_final_count.count(),
                "wrong_answers_list": {
                    "exit_question": reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct()
                },
                "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
                "submitted_for_evaluation": len(submit_ids)
            }
            data.update(task_status)
            return data
        else:
            return None
            # return "Sorry ! Question's not found."

    def get_task_7_instruction(self, obj):
        if obj.number_of_points == "points_20":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_7"
                ).first()
            ).data

            # essay_question_order_details

            accepted_ids = obj.essay_question_order_details.filter(
                status="Accepted", question__main_task_number="task_7"
            ).values_list("question", flat=True)
            submit_ids = obj.essay_question_order_details.filter(
                status="Submitted", question__main_task_number="task_7"
            ).values_list("question", flat=True)
            final_count = obj.essay_question_order_details.exclude(
                question__in=accepted_ids,
            ).filter(question__main_task_number="task_7")
            final_count = final_count.exclude(
                question__in=submit_ids,
            )

            reject_question_final_count = (
                final_count.filter(status="Rejected", question=OuterRef("question"))
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            reject_question_final_count = final_count.filter(
                create_time=Subquery(reject_question_final_count)
            )
            total_questions = 5
            task_status = {
                "total_questions": total_questions,
                "correct_answers": len(accepted_ids),
                "wrong_answers": reject_question_final_count.count(),
                "wrong_answers_list": {
                    "essay_question": reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct()
                },
                "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
                "submitted_for_evaluation": len(submit_ids)
            }
            data.update(task_status)
            return data
        return None

    def get_task_8_instruction(self, obj):
        if obj.number_of_points == "points_20":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_8"
                ).first()
            ).data

            accepted_ids = obj.essay_question_order_details.filter(
                status="Accepted", question__main_task_number="task_8"
            ).values_list("question", flat=True)
            submit_ids = obj.essay_question_order_details.filter(
                status="Submitted", question__main_task_number="task_8"
            ).values_list("question", flat=True)
            final_count = obj.essay_question_order_details.exclude(
                question__in=accepted_ids,
            ).filter(question__main_task_number="task_8")
            final_count = final_count.exclude(
                question__in=submit_ids, question__main_task_number="task_8"
            )

            reject_question_final_count = (
                final_count.filter(status="Rejected", question=OuterRef("question"))
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            reject_question_final_count = final_count.filter(
                create_time=Subquery(reject_question_final_count)
            )
            total_questions = 5
            task_status = {
                "total_questions": total_questions,
                "correct_answers": len(accepted_ids),
                "wrong_answers": reject_question_final_count.count(),
                "wrong_answers_list": {
                    "essay_question": reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct()
                },
                "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
                "submitted_for_evaluation": len(submit_ids)
            }
            data.update(task_status)
            return data
        return None

    def get_task_9_instruction(self, obj):
        if obj.number_of_points == "points_20":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_9"
                ).first()
            ).data

            # short_question_order_details

            short_question_accepted_ids = obj.short_question_order_details.filter(
                status="Accepted", question__main_task_number="task_9"
            ).values_list("question", flat=True)
            short_question_submit_ids = obj.short_question_order_details.filter(
                status="Submitted"
            ).values_list("question", flat=True)
            short_question_final_count = obj.short_question_order_details.exclude(
                question__in=short_question_accepted_ids,
            ).filter(question__main_task_number="task_9")
            short_question_final_count = short_question_final_count.exclude(
                question__in=short_question_submit_ids,
            )

            short_reject_question_final_count = (
                short_question_final_count.filter(
                    status="Rejected", question=OuterRef("question")
                )
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            short_reject_question_final_count = short_question_final_count.filter(
                create_time=Subquery(short_reject_question_final_count)
            )

            # dropdown_question_order_details

            dropdown_question_accepted_ids = obj.dropdown_question_order_details.filter(
                status="Accepted", question__main_task_number="task_9"
            ).values_list("question", flat=True)
            dropdown_question_submit_ids = obj.dropdown_question_order_details.filter(
                status="Submitted"
            ).values_list("question", flat=True)
            dropdown_question_final_count = obj.dropdown_question_order_details.exclude(
                question__in=dropdown_question_accepted_ids,
            ).filter(question__main_task_number="task_9")
            dropdown_question_final_count = dropdown_question_final_count.exclude(
                question__in=dropdown_question_submit_ids,
            )
            dropdown_reject_question_final_count = (
                dropdown_question_final_count.filter(
                    status="Rejected", question=OuterRef("question")
                )
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            dropdown_reject_question_final_count = dropdown_question_final_count.filter(
                create_time=Subquery(dropdown_reject_question_final_count)
            )

            # numeric_question_order_details

            numeric_question_question_accepted_ids = (
                obj.numeric_question_order_details.filter(
                    status="Accepted", question__main_task_number="task_9"
                ).values_list("question", flat=True)
            )
            numeric_question_submit_ids = obj.numeric_question_order_details.filter(
                status="Submitted"
            ).values_list("question", flat=True)
            numeric_question_final_count = obj.numeric_question_order_details.exclude(
                question__in=numeric_question_question_accepted_ids,
            ).filter(question__main_task_number="task_9")
            numeric_question_final_count = numeric_question_final_count.exclude(
                question__in=numeric_question_submit_ids,
            )

            numeric_reject_question_final_count = (
                numeric_question_final_count.filter(
                    status="Rejected", question=OuterRef("question")
                )
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            numeric_reject_question_final_count = numeric_question_final_count.filter(
                create_time=Subquery(numeric_reject_question_final_count)
            )

            # percentage_question_order_details

            percentage_question_accepted_ids = (
                obj.percentage_question_order_details.filter(
                    status="Accepted", question__main_task_number="task_9"
                ).values_list("question", flat=True)
            )
            percentage_question_submit_ids = (
                obj.percentage_question_order_details.filter(
                    status="Submitted"
                ).values_list("question", flat=True)
            )
            percentage_question_final_count = (
                obj.percentage_question_order_details.exclude(
                    question__in=percentage_question_accepted_ids,
                ).filter(question__main_task_number="task_9")
            )
            percentage_question_final_count = (
                percentage_question_final_count.exclude(
                    question__in=percentage_question_submit_ids,
                ))
            #     .filter(status="Rejected", question=OuterRef("question"))
            #     .order_by("-create_time")
            #     .values_list("create_time")[:1]
            # )

            percentage_reject_question_final_count = (
                percentage_question_final_count.filter(
                    status="Rejected", question=OuterRef("question")
                )
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            percentage_reject_question_final_count = (
                percentage_question_final_count.filter(
                    create_time=Subquery(percentage_reject_question_final_count)
                )
            )
            total_questions = 25
            accepted_ids = len(short_question_accepted_ids) + len(dropdown_question_accepted_ids) + len(
                numeric_question_question_accepted_ids) + len(percentage_question_accepted_ids)
            submit_ids = len(short_question_submit_ids) + len(dropdown_question_submit_ids) + len(
                numeric_question_submit_ids) + len(percentage_question_submit_ids)
            task_status = {
                "total_questions": total_questions,
                "correct_answers": len(short_question_accepted_ids)
                                   + len(dropdown_question_accepted_ids)
                                   + len(numeric_question_question_accepted_ids)
                                   + len(percentage_question_accepted_ids),
                "wrong_answers": short_reject_question_final_count.count()
                                 + dropdown_reject_question_final_count.count()
                                 + numeric_reject_question_final_count.count()
                                 + percentage_reject_question_final_count.count(),
                "wrong_answers_list": {
                    "short_question": short_reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct(),
                    "dropdown_question": dropdown_reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct(),
                    "numeric_question": numeric_reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct(),
                    "percentage_question": percentage_reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct(),
                },
                "not_submitted": total_questions - accepted_ids - submit_ids,
                "submitted_for_evaluation": submit_ids
            }
            data.update(task_status)
            return data
        else:
            return None

    def get_task_10_instruction(self, obj):
        if obj.number_of_points == "points_20":
            data = TaskInstructionsListSerializer(
                obj.project.task_instructions_question_projects.filter(
                    main_task_number="task_10"
                ).first()
            ).data
            accepted_ids = obj.exit_question_order_details.filter(
                status="Accepted", question__main_task_number="task_10"
            ).values_list("question", flat=True)
            submit_ids = obj.exit_question_order_details.filter(
                status="Submitted", question__main_task_number="task_10"
            ).values_list("question", flat=True)
            final_count = obj.exit_question_order_details.exclude(
                question__in=accepted_ids,
            ).filter(question__main_task_number="task_10")
            final_count = final_count.exclude(
                question__in=submit_ids,
            )

            reject_question_final_count = (
                final_count.filter(status="Rejected", question=OuterRef("question"))
                .order_by("-create_time")
                .values_list("create_time")[:1]
            )
            reject_question_final_count = final_count.filter(
                create_time=Subquery(reject_question_final_count)
            )
            total_questions = 20
            task_status = {
                "total_questions": 20,
                "correct_answers": len(accepted_ids),
                "wrong_answers": reject_question_final_count.count(),
                "wrong_answers_list": {
                    "exit_question": reject_question_final_count.values_list(
                        "id", flat=True
                    ).distinct()
                },
                "not_submitted": total_questions - len(accepted_ids) - len(submit_ids),
                "submitted_for_evaluation": len(submit_ids)
            }
            data.update(task_status)
            return data
        else:
            return None


ANSWERS_STATUS = (
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
)

MODEL_NAME = (
    ("essay_question", "AnswersEssayQuestionSerializer"),
    ("upload_photo_question", "AnswersUploadPhotoQuestionSerializer"),
    ("short_question", "AnswersShortQuestionSerializer"),
    ("numeric_question", "AnswersNumericQuestionSerializer"),
    ("dropdown_question", "AnswersDropDownQuestionSerializer"),
    ("percentage_question", "AnswersPercentageQuestionSerializer"),
    ("mcq_question", "AnswersMCQQuestionSerializer"),
)


class EvaluationQuestionAnswersSerializer(serializers.Serializer):
    question_answers = serializers.IntegerField(required=True)
    model_name = serializers.ChoiceField(choices=MODEL_NAME, required=True)
    status = serializers.ChoiceField(choices=ANSWERS_STATUS, required=True)
    reject_reason = serializers.CharField(required=False)


class Task3PhotoQuestionSerializer(serializers.Serializer):
    order_details_id = serializers.IntegerField(required=True)
    survey_number = serializers.IntegerField(required=True)
    # status = serializers.CharField(required=True, min_length=1, max_length=100)
    status = serializers.ChoiceField(choices=ANSWERS_STATUS, required=True)


class Task3McqQuestionSerializer(serializers.Serializer):
    order_details_id = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=ANSWERS_STATUS, required=True)


class EditEvaluationAnswersSerializer(serializers.Serializer):
    question_answers = serializers.IntegerField(required=True)
    model_name = serializers.ChoiceField(choices=MODEL_NAME, required=True)
    answer = serializers.CharField(required=True)


POINT = (
    ("points_20", "20 Points"),
    ("points_10", "10 Points"),
    ("points_05", "05 Points"),
)

MAIN_TASK_NUMBER = (
    ("task_2", "Task – 2"),
    ("task_5", "Task – 5"),
    ("task_6", "Task – 6"),
    ("task_7", "Task – 7"),
    ("task_8", "Task – 8"),
)


class GetEssayEvaluationQuestionSerializer(serializers.Serializer):
    order_details = serializers.IntegerField(required=True)
    number_of_points = serializers.ChoiceField(choices=POINT, required=True)
    task_number = serializers.ChoiceField(choices=MAIN_TASK_NUMBER, required=True)

    def validate(self, data):
        number_of_points = data["number_of_points"]
        task_number = data["task_number"]

        # Define a dictionary to map the valid tasks for each number_of_points
        valid_tasks = {
            "points_05": ["task_2"],
            "points_10": ["task_2", "task_5"],
            "points_20": ["task_2", "task_5", "task_6", "task_7", "task_8"],
        }

        if task_number not in valid_tasks.get(number_of_points, []):
            raise serializers.ValidationError(
                "Invalid task number for the selected number of points."
            )

        return data


class Task4EvaluationQuestionSerializer(serializers.Serializer):
    order_details = serializers.IntegerField(required=True)
