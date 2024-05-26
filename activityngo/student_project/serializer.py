from datetime import datetime

import pytz
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from activityngo.project.models import Project
from activityngo.question_types.serializers import (
    TaskInstructionsListSerializer,
    VideoQuestionSerializer,
)
from activityngo.student_project.models import (
    DropDownQuestionAnswers,
    EssayQuestionAnswers,
    ExitQuestionAnswers,
    MCQQuestionAnswers,
    NumericQuestionAnswers,
    PercentageQuestionAnswers,
    ShortQuestionAnswers,
    StudentTaskStatus,
    SurveysDetails,
    UploadPhotoQuestionAnswers,
    VideoQuestionAnswers,
)


class EmptyStudentProjectDetailsSerializer(serializers.Serializer):
    pass


class StudentPurchaseProjectListSerializer(serializers.ModelSerializer):
    subscribed_on = serializers.SerializerMethodField()
    expired_on = serializers.SerializerMethodField()
    is_expire = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()
    number_of_points = serializers.SerializerMethodField()
    task_status = serializers.SerializerMethodField()
    total_task = serializers.SerializerMethodField()
    field_visit_mandation = serializers.SerializerMethodField()
    scheduling_field_visit_by_ngo = serializers.SerializerMethodField()
    can_students_visit_field_by_themselves = serializers.SerializerMethodField()
    places_that_can_be_considered_for_field_visit = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "subscribed_on",
            "expired_on",
            "is_expire",
            "order_id",
            "number_of_points",
            "days_of_20_point",
            "days_of_10_point",
            "days_of_05_point",
            "task_status",
            "total_task",
            "field_visit_mandation",
            "scheduling_field_visit_by_ngo",
            "can_students_visit_field_by_themselves",
            "places_that_can_be_considered_for_field_visit",
        ]

    def get_task_status(self, obj):
        try:
            return StudentTaskStatusSerializer(
                StudentTaskStatus.objects.filter(
                    order_details=obj.product_order_details.get(
                        order__user=self.context["request"].user,
                        is_expire=False,
                        order__is_temp_order=False,
                    ).id
                ).first()
            ).data
        except:
            return ""

    def get_field_visit_mandation(self, obj):
        try:
            return obj.projects_details.field_visit_mandation
        except:
            return ""

    def get_scheduling_field_visit_by_ngo(self, obj):
        try:
            return obj.projects_details.scheduling_field_visit_by_ngo
        except:
            return ""

    def get_can_students_visit_field_by_themselves(self, obj):
        try:
            return obj.projects_details.can_students_visit_field_by_themselves
        except:
            return ""

    def get_places_that_can_be_considered_for_field_visit(self, obj):
        try:
            return obj.projects_details.places_that_can_be_considered_for_field_visit
        except:
            return ""

    def get_subscribed_on(self, obj):
        try:
            return (
                obj.product_order_details.filter(
                    order__user=self.context["request"].user,
                    order__is_temp_order=False,
                    is_expire=False,
                )
                .order_by("-create_time")
                .first()
                .order.create_time
            )
        except:
            return ""

    def get_number_of_points(self, obj):
        try:
            return (
                obj.product_order_details.filter(
                    order__user=self.context["request"].user,
                    order__is_temp_order=False,
                    is_expire=False,
                )
                .order_by("-create_time")
                .first()
                .number_of_points
            )
        except:
            return ""

    def get_expired_on(self, obj):
        try:
            expire_instance = obj.product_order_details.filter(
                order__user=self.context["request"].user,
                order__is_temp_order=False,
                is_expire=False,
            ).order_by("-create_time").first()

            if expire_instance:
                # Format expiration datetime in ISO 8601 format
                expire_datetime = expire_instance.expire_on.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                return expire_datetime
        except:
            pass

        return ""
        # try:
        #     return (
        #         obj.product_order_details.filter(
        #             order__user=self.context["request"].user,
        #             order__is_temp_order=False,
        #             is_expire=False,
        #         )
        #         .order_by("-create_time")
        #         .first()
        #         .expire_on
        #     )
        # except:
        #     return ""

    def get_is_expire(self, obj):
        try:
            return (
                obj.product_order_details.filter(
                    order__user=self.context["request"].user,
                    order__is_temp_order=False,
                    is_expire=False,
                )
                .order_by("-create_time")
                .first()
                .is_expire
            )
        except:
            return ""

    def get_order_id(self, obj):
        try:
            return (
                obj.product_order_details.filter(
                    order__user=self.context["request"].user, is_expire=False
                )
                .order_by("-create_time")
                .first()
                .id
            )
        except:
            return ""

    def get_total_task(self, obj):
        try:
            project = (
                obj.product_order_details.filter(
                    order__user=self.context["request"].user
                )
                .order_by("create_time")
                .first()
            )
            return (
                10
                if project.number_of_points == "points_20"
                else 6 if project.number_of_points == "points_10" else 4
            )
        except:
            return None


class StudentPurchaseProjectDetailsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    project_code = serializers.SerializerMethodField()
    aicte_category = serializers.SerializerMethodField()
    vtu_category = serializers.SerializerMethodField()
    mode = serializers.SerializerMethodField()
    beneficiary = serializers.SerializerMethodField()
    subscribed_date = serializers.SerializerMethodField()
    expired_date = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    number_of_points = serializers.SerializerMethodField()

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

    task_1 = serializers.SerializerMethodField()

    task_status = serializers.SerializerMethodField()
    franchise_ngo_name = serializers.SerializerMethodField()
    issue_of_certificate = serializers.SerializerMethodField()
    issue_of_report = serializers.SerializerMethodField()
    mode_of_receiving_report_and_certificate = serializers.SerializerMethodField()
    report_file = serializers.SerializerMethodField()
    field_visit_mandation = serializers.SerializerMethodField()
    scheduling_field_visit_by_ngo = serializers.SerializerMethodField()
    can_students_visit_field_by_themselves = serializers.SerializerMethodField()
    places_that_can_be_considered_for_field_visit = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "franchise_ngo_name",
            "expire_duration_in_days_by_students",
            "issue_of_certificate",
            "issue_of_report",
            "mode_of_receiving_report_and_certificate",
            "expire_duration_in_days_by_evaluate",
            "category_name",
            "project_code",
            "aicte_category",
            "vtu_category",
            "mode",
            "days_of_20_point",
            "days_of_10_point",
            "days_of_05_point",
            "beneficiary",
            "subscribed_date",
            "expired_date",
            "days_remaining",
            "number_of_points",
            "task_status",
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
            "task_1",
            "report_file",
            "field_visit_mandation",
            "scheduling_field_visit_by_ngo",
            "can_students_visit_field_by_themselves",
            "places_that_can_be_considered_for_field_visit"
        ]

    def get_field_visit_mandation(self, obj):
        try:
            return obj.projects_details.field_visit_mandation
        except:
            return ""

    def get_scheduling_field_visit_by_ngo(self, obj):
        try:
            return obj.projects_details.scheduling_field_visit_by_ngo
        except:
            return ""

    def get_can_students_visit_field_by_themselves(self, obj):
        try:
            return obj.projects_details.can_students_visit_field_by_themselves
        except:
            return ""

    def get_places_that_can_be_considered_for_field_visit(self, obj):
        try:
            return obj.projects_details.places_that_can_be_considered_for_field_visit
        except:
            return ""

    def get_franchise_ngo_name(self, obj):
        try:
            return obj.franchise_ngo_name.ngo_name
        except:
            return ""

    def get_issue_of_certificate(self, obj):
        try:
            return obj.projects_details.issue_of_certificate
        except:
            return ""

    def get_issue_of_report(self, obj):
        try:
            return obj.projects_details.issue_of_report
        except:
            return ""

    def get_mode_of_receiving_report_and_certificate(self, obj):
        try:
            return obj.projects_details.mode_of_receiving_report_and_certificate
        except:
            return ""

    def get_task_status(self, obj):
        try:
            return StudentTaskStatusSerializer(
                StudentTaskStatus.objects.filter(
                    order_details=self.context["order_details"]
                ).first()
            ).data
        except:
            return ""

    def get_category_name(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_project_code(self, obj):
        return ""

    def get_aicte_category(self, obj):
        return ""

    def get_vtu_category(self, obj):
        return ""

    def get_mode(self, obj):
        try:
            return obj.projects_details.mode
        except:
            return ""

    def get_beneficiary(self, obj):
        try:
            return obj.projects_details.beneficiary_in_society
        except:
            return ""

    def get_subscribed_date(self, obj):
        return self.context["order_details"].order.create_time

    def get_expired_date(self, obj):
        try:
            expire_on = self.context["order_details"].expire_on
            formatted_expire_on = expire_on.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            return formatted_expire_on
        except:
            return None

    def get_report_file(self, obj):
        try:
            user = self.context["request"].user
            if user is not None and user.user_type == "student":
                if self.context["order_details"].activity_status == "approve_complete" or self.context[
                    "order_details"].activity_status == "complete":
                    return self.context["order_details"].report_file.url
                else:
                    return None
            return self.context["order_details"].report_file.url
        except:
            return None

    def get_days_remaining(self, obj):
        expire_on_utc = self.context["order_details"].expire_on
        current_datetime = datetime.now(pytz.utc)

        # Convert current_datetime to UTC if it's not already
        current_datetime_utc = current_datetime.astimezone(pytz.utc)

        days_difference = (expire_on_utc - current_datetime_utc).days
        return days_difference if days_difference > 0 else 0

    def get_number_of_points(self, obj):
        return self.context["order_details"].number_of_points

    def get_task_1_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_1"
            ).first()
        ).data

    def get_task_2_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_2"
            ).first()
        ).data

    def get_task_3_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_3"
            ).first()
        ).data

    def get_task_4_instruction(self, obj):
        if self.context["number_of_points"] == "points_05":
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_10"
                ).first()
            ).data
        else:
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_4"
                ).first()
            ).data

    def get_task_5_instruction(self, obj):
        if (
                self.context["number_of_points"] == "points_20"
                or self.context["number_of_points"] == "points_10"
        ):
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_5"
                ).first()
            ).data
        # return "Sorry ! Question's not found."
        return None

    def get_task_6_instruction(self, obj):
        if self.context["number_of_points"] == "points_20":
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_6"
                ).first()
            ).data
        elif self.context["number_of_points"] == "points_10":
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_10"
                ).first()
            ).data
        else:
            return None
            # return "Sorry ! Question's not found."

    def get_task_7_instruction(self, obj):
        if self.context["number_of_points"] == "points_20":
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_7"
                ).first()
            ).data
        return None
        # return "Sorry ! Question's not found."

    def get_task_8_instruction(self, obj):
        if self.context["number_of_points"] == "points_20":
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_8"
                ).first()
            ).data
        return None
        # return "Sorry ! Question's not found."

    def get_task_9_instruction(self, obj):
        if self.context["number_of_points"] == "points_20":
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_9"
                ).first()
            ).data
        else:
            return None
            # return "Sorry ! Question's not found."

    def get_task_10_instruction(self, obj):
        if self.context["number_of_points"] == "points_20":
            return TaskInstructionsListSerializer(
                obj.task_instructions_question_projects.filter(
                    main_task_number="task_10"
                ).first()
            ).data
        else:
            return None
            # return "Sorry ! Question's not found."

    def get_task_1(self, obj):
        return VideoQuestionSerializer(
            obj.video_question_projects.filter(is_active=1).order_by("sub_task_number")[
            :2
            ],
            many=True,
            context={"request": self.context["request"]},
        ).data


class AnswersVideoQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoQuestionAnswers
        fields = ["question", "order_details"]
        extra_kwargs = {
            # 'user': {'required': True},
            "question": {"required": True},
            "order_details": {"required": True},
        }

    def validate(self, attrs):
        if VideoQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        attrs["user"] = self.context["request"].user
        attrs["status"] = "Submitted"
        return super().validate(attrs)


class AnswersEssayQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {"survey_number": {"required": True}}

    def validate(self, attrs):
        if EssayQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        attrs["user"] = self.context["request"].user
        attrs["status"] = "Submitted"
        return super().validate(attrs)


class AnswersUploadPhotoQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadPhotoQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {"survey_number": {"required": True}}

    def validate(self, attrs):
        if UploadPhotoQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        attrs["user"] = self.context["request"].user
        attrs["status"] = "Submitted"
        return super().validate(attrs)


class AnswersShortQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {"survey_number": {"required": True}}

    def validate(self, attrs):
        if ShortQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        elif (
                not
                attrs.get("question").answer_character_minimum_limit
                <= len(attrs.get("answer"))
                <= attrs.get("question").answer_character_maximum_limit
        ):
            raise serializers.ValidationError(
                _(
                    f"Your answer to {attrs.get('question').question} should be between {attrs.get('question').answer_character_minimum_limit} and {attrs.get('question').answer_character_maximum_limit}."
                )
            )

        attrs["user"] = self.context["request"].user
        if attrs.get("question").sub_task_number == 2 and attrs.get("question").main_task_number == 'task_9':
            attrs["status"] = "Accepted"
        else:
            attrs["status"] = "Submitted"
        return super().validate(attrs)


class AnswersNumericQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumericQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {"survey_number": {"required": True}}

    def validate(self, attrs):
        if NumericQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )

        elif (
                not
                attrs.get("question").answer_character_minimum_limit <= attrs.get("answer") <= attrs.get(
                    "question").answer_character_maximum_limit
        ):
            raise serializers.ValidationError(
                _(
                    f"Your answer to {attrs.get('question').question} should be between {attrs.get('question').answer_character_minimum_limit} and {attrs.get('question').answer_character_maximum_limit}."
                )
            )
        attrs["user"] = self.context["request"].user
        if attrs.get("question").main_task_number == 'task_9':
            attrs["status"] = "Accepted"
        else:
            attrs["status"] = "Submitted"
        return super().validate(attrs)


class AnswersDropDownQuestionSerializer(serializers.ModelSerializer):
    # answer = serializers.ListSerializer(child=serializers.CharField(), required=True, allow_null=True,
    #                                     allow_empty=True)

    class Meta:
        model = DropDownQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {
            "question": {"required": True},
            "order_details": {"required": True},
            "answer": {"required": True},
            "survey_number": {"required": True},
        }

    def validate(self, attrs):
        if DropDownQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        attrs["user"] = self.context["request"].user
        if attrs.get("question").main_task_number == 'task_9':
            attrs["status"] = "Accepted"
        else:
            attrs["status"] = "Submitted"
        return super().validate(attrs)

    # def create(self, validated_data):
    #     answers = validated_data.pop("answer", [])
    #     obj = super().create(validated_data)
    #
    #     # Insert all selected answers into DropDownSelectedOptions Tables
    #     for answer in answers:
    #         DropDownSelectedOptions.objects.create(
    #             question_answers=obj, answer=answer
    #         )
    #
    #     return obj


class AnswersPercentageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {"survey_number": {"required": True}}

    def validate(self, attrs):
        if PercentageQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        elif (
                not
                attrs.get("question").answer_character_minimum_limit <= attrs.get("answer") <= attrs.get(
                    "question").answer_character_maximum_limit
        ):
            raise serializers.ValidationError(
                _(
                    f"Your answer to {attrs.get('question').question} should be between {attrs.get('question').answer_character_minimum_limit} and {attrs.get('question').answer_character_maximum_limit}."
                )
            )
        attrs["user"] = self.context["request"].user
        if attrs.get("question").main_task_number == 'task_9':
            attrs["status"] = "Accepted"
        else:
            attrs["status"] = "Submitted"
        return super().validate(attrs)


class AnswersMCQQuestionSerializer(serializers.ModelSerializer):
    # answer = serializers.ListSerializer(child=serializers.CharField(), required=True, allow_null=True,
    #                                     allow_empty=True)

    class Meta:
        model = MCQQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {
            "question": {"required": True},
            "order_details": {"required": True},
            "survey_number": {"required": True},
            "answer": {"required": True},
        }

    def validate(self, attrs):
        if MCQQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        attrs["user"] = self.context["request"].user
        attrs["status"] = "Submitted"
        return super().validate(attrs)

    # def create(self, validated_data):
    #     answers = validated_data.pop("answer", [])
    #     obj = super().create(validated_data)
    #
    #     # Insert all selected answers into MCQSelectedOptions Tables
    #     for answer in answers:
    #         MCQSelectedOptions.objects.create(
    #             question_answers=obj, answer=answer
    #         )
    #
    #     return obj


class AnswersExitQuestionSerializer(serializers.ModelSerializer):
    # answer = serializers.ListSerializer(child=serializers.CharField(), required=True, allow_null=True,
    #                                     allow_empty=True)

    class Meta:
        model = ExitQuestionAnswers
        fields = ["question", "order_details", "answer", "survey_number"]
        extra_kwargs = {"survey_number": {"required": True}}

    def validate(self, attrs):
        # if ExitQuestionAnswers.objects.filter(question=attrs['question'], user=self.context['request'].user,
        #                                       order_details=attrs['order_details'],
        #                                       survey_number=attrs['survey_number'],Q(status="Accepted") | Q(status="Submitted")).exists():
        if ExitQuestionAnswers.objects.filter(
                Q(status="Accepted") | Q(status="Submitted"),
                question=attrs["question"],
                user=self.context["request"].user,
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
        ).exists():
            raise serializers.ValidationError(
                _(
                    "Your answer has already been successfully submitted. Please avoid "
                    "sending the same answer repeatedly."
                )
            )
        attrs["user"] = self.context["request"].user
        attrs["status"] = "Submitted"
        return super().validate(attrs)

    # def create(self, validated_data):
    #     answers = validated_data.pop("answer", [])
    #     obj = super().create(validated_data)
    #
    #     # Insert all selected answers into ExitSelectedOptions Tables
    #     for answer in answers:
    #         ExitSelectedOptions.objects.create(
    #             question_answers=obj, answer=answer
    #         )
    #
    #     return obj


class SurveysDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveysDetails
        fields = ["order_details", "survey_number", "main_task_number"]

    def validate(self, attrs):
        if SurveysDetails.objects.filter(
                order_details=attrs["order_details"],
                survey_number=attrs["survey_number"],
                main_task_number=attrs["main_task_number"],
                user=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("Task survey already added.")
        attrs["user"] = self.context["request"].user
        return super().validate(attrs)


class StudentTaskStatusSerializer(serializers.ModelSerializer):
    submit_time_task_1 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_2 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_3 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_4 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_5 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_6 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_7 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_8 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_9 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    submit_time_task_10 = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')

    class Meta:
        model = StudentTaskStatus
        fields = [
            "id",
            "order_details",
            "create_time",
            "update_time",
            "task1",
            "task2",
            "task3",
            "task3_submissions",
            "task4",
            "task5",
            "task6",
            "task7",
            "task8",
            "task9",
            "task10",
            "submit_time_task_1",
            "submit_time_task_2",
            "submit_time_task_3",
            "submit_time_task_4",
            "submit_time_task_5",
            "submit_time_task_6",
            "submit_time_task_7",
            "submit_time_task_8",
            "submit_time_task_9",
            "submit_time_task_10",
        ]


STATUS_OF_ANSWER = (
    ("Accepted", "Accepted"),
    ("Submitted", "Submitted"),
)


class ShortQuestionAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    order_details = serializers.IntegerField(required=True)
    answer = serializers.CharField(required=True)
    survey_number = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=STATUS_OF_ANSWER, required=False)


class NumericQuestionAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    order_details = serializers.IntegerField(required=True)
    answer = serializers.FloatField(required=True)
    survey_number = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=STATUS_OF_ANSWER, required=False)


class ListFieldSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class McqQuestionAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    order_details = serializers.IntegerField(required=True)
    answer = serializers.IntegerField(required=True)
    # answer = ListFieldSerializer(child=serializers.CharField(), allow_empty=False)
    survey_number = serializers.IntegerField(required=True)


class DropdownQuestionAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    order_details = serializers.IntegerField(required=True)
    answer = serializers.IntegerField(required=True)
    survey_number = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=STATUS_OF_ANSWER, required=False)


class PercentageQuestionAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    order_details = serializers.IntegerField(required=True)
    answer = serializers.FloatField(required=True)
    survey_number = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=STATUS_OF_ANSWER, required=False)


class SurveyTask3Serializer(serializers.Serializer):
    short_question = ShortQuestionAnswerSerializer(required=True)
    numeric_question = NumericQuestionAnswerSerializer(required=True)
    mcq_question = serializers.ListField(
        child=McqQuestionAnswerSerializer(required=True),
        required=True,
        min_length=17,
        max_length=17,
        error_messages={
            "min_length": "Please submit all answers.",
            "max_length": "Please submit all answers.",
        },
    )


class SurveyTask9Serializer(serializers.Serializer):
    short_question = serializers.ListField(
        child=ShortQuestionAnswerSerializer(required=True),
        required=True,
        min_length=2,
        max_length=2,
        error_messages={
            'min_length': 'Please submit all answers.',
            'max_length': 'Please submit all answers.',
        },
    )
    dropdown_question = serializers.ListField(
        child=DropdownQuestionAnswerSerializer(required=True),
        required=True,
        min_length=2,
        max_length=2,
        error_messages={
            'min_length': 'Please submit all answers.',
            'max_length': 'Please submit all answers.',
        },
    )
    numeric_question = serializers.ListField(
        child=NumericQuestionAnswerSerializer(required=True),
        required=True,
        min_length=17,
        max_length=17,
        error_messages={
            'min_length': 'Please submit all answers.',
            'max_length': 'Please submit all answers.',
        },
    )
    percentage_question = serializers.ListField(
        child=PercentageQuestionAnswerSerializer(required=True),
        required=True,
        min_length=4,
        max_length=4,
        error_messages={
            'min_length': 'Please submit all answers.',
            'max_length': 'Please submit all answers.',
        },
    )
