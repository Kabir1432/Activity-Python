from django.db.models import Avg
from rest_framework import serializers
from django.db import transaction
from activityngo.project.models import (Project, ProjectDetails, SpecialPower,
                                        StudentFeedback)
from activityngo.question_types.serializers import (
    DropdownQuestionSerializer, EssayQuestionSerializer,
    ExitTestQuestionSerializer, MCQQuestionSerializer,
    NumericQuestionSerializer, PercentageQuestionSerializer,
    ShortAnswerQuestionSerializer, TaskInstructionsListSerializer,
    UploadPhotoQuestionSerializer, VideoQuestionSerializer)


class ProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetails
        fields = (
            "id",
            "project",
            "mode",
            "beneficiary_in_society",
            "number_of_tasks",
            "field_visit_mandation",
            "scheduling_field_visit_by_ngo",
            "can_students_visit_field_by_themselves",
            "places_that_can_be_considered_for_field_visit",
            "issue_of_certificate",
            "issue_of_report",
            "mode_of_receiving_report_and_certificate",
        )
        extra_kwargs = {
            "project": {"required": True},
            "mode": {"required": True},
            "beneficiary_in_society": {"required": True},
            "number_of_tasks": {"required": True},
            "field_visit_mandation": {"required": True},
            "scheduling_field_visit_by_ngo": {"required": True},
            "can_students_visit_field_by_themselves": {"required": True},
            "places_that_can_be_considered_for_field_visit": {"required": True},
            "issue_of_certificate": {"required": True},
            "issue_of_report": {"required": True},
            "mode_of_receiving_report_and_certificate": {"required": True},
        }


class ProjectListSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "category",
            "category_name",
            "subscription_price",
            "gst_inclusive",
            "type",
            "price_of_20_point",
            "price_of_10_point",
            "price_of_05_point",
            "days_of_20_point",
            "days_of_10_point",
            "days_of_05_point",
            "rating",
            "is_active"
        ]

    def get_type(self, obj):
        try:
            return obj.type.name
        except:
            return ""

    def get_category_name(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_rating(self, obj):
        try:
            avg_rating = (
                obj.projects_feedback.all()
                .aggregate(avg_rating=Avg("rating"))
                .get("avg_rating")
            )
            return avg_rating
        except:
            return ""


class ProjectSerializer(serializers.ModelSerializer):
    projects_details = ProjectDetailsSerializer(read_only=True)
    task_1 = serializers.SerializerMethodField()
    task_2 = serializers.SerializerMethodField()
    task_3 = serializers.SerializerMethodField()
    task_4 = serializers.SerializerMethodField()
    task_5 = serializers.SerializerMethodField()
    task_6 = serializers.SerializerMethodField()
    task_7 = serializers.SerializerMethodField()
    task_8 = serializers.SerializerMethodField()
    task_9 = serializers.SerializerMethodField()
    task_10 = serializers.SerializerMethodField()
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
    category_name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    franchise_ngo_names = serializers.CharField(source="franchise_ngo_name.ngo_name", read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "franchise_ngo_name",
            "franchise_ngo_names",
            "category",
            "category_name",
            # "subscription_price",
            "type",
            "title",
            "expire_duration_in_days_by_students",
            "expire_duration_in_days_by_evaluate",
            "subscription_price",
            "minimum_number_of_days",
            "gst_inclusive",
            "price_of_20_point",
            "price_of_10_point",
            "price_of_05_point",
            "days_of_20_point",
            "days_of_10_point",
            "days_of_05_point",
            "projects_details",
            "task_1",
            "is_basic_details",
            "rating",
            "is_project_details",
            "is_task_summary",
            "is_task_1",
            "is_task_2",
            "is_task_3",
            "is_task_4",
            "is_task_5",
            "is_task_6",
            "is_task_7",
            "is_task_8",
            "is_task_9",
            "is_task_10",
            "is_active",
            "task_2",
            "task_3",
            "task_4",
            "task_5",
            "task_6",
            "task_7",
            "task_8",
            "task_9",
            "task_10",
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
            "is_visible",
        )
        extra_kwargs = {
            "number_of_points": {"required": True},
            "number_of_hours": {"required": True},
            "franchise_ngo_name": {"required": True},
            "category": {"required": True},
            "type": {"required": True},
            "title": {"required": True},
            "expire_duration_in_days_by_students": {"required": True},
            "expire_duration_in_days_by_evaluate": {"required": True},
            # "subscription_price": {"required": True},
            # "minimum_number_of_days": {"required": True},
            "gst_inclusive": {"required": True},
            "price_of_20_point": {"required": True},
            "price_of_10_point": {"required": True},
            "price_of_05_point": {"required": True},
            "days_of_20_point": {"required": True},
            "days_of_10_point": {"required": True},
            "days_of_05_point": {"required": True},
        }

    def get_category_name(self, obj):
        try:
            return obj.category.name
        except:
            return ""

    def get_type(self, obj):
        try:
            return obj.type.name
        except:
            return ""

    def get_rating(self, obj):
        try:
            avg_rating = (
                obj.projects_feedback.all()
                .aggregate(avg_rating=Avg("rating"))
                .get("avg_rating")
            )
            return avg_rating
        except:
            return ""

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
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_4"
            ).first()
        ).data

    def get_task_5_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_5"
            ).first()
        ).data

    def get_task_6_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_6"
            ).first()
        ).data

    def get_task_7_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_7"
            ).first()
        ).data

    def get_task_8_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_8"
            ).first()
        ).data

    def get_task_9_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_9"
            ).first()
        ).data

    def get_task_10_instruction(self, obj):
        return TaskInstructionsListSerializer(
            obj.task_instructions_question_projects.filter(
                main_task_number="task_10"
            ).first()
        ).data

    def get_task_1(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            return VideoQuestionSerializer(
                obj.video_question_projects.all().order_by("sub_task_number")[:2],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            return VideoQuestionSerializer(
                obj.video_question_projects.filter(is_active=1).order_by(
                    "sub_task_number"
                )[:2],
                many=True,
                context={"request": self.context["request"]},
            ).data

    def get_task_2(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            return EssayQuestionSerializer(
                obj.essay_question_projects.filter(main_task_number="task_2").order_by(
                    "sub_task_number"
                )[:20],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            return EssayQuestionSerializer(
                obj.essay_question_projects.filter(
                    is_active=1, main_task_number="task_2"
                ).order_by("sub_task_number")[:20],
                many=True,
                context={"request": self.context["request"]},
            ).data

    def get_task_3(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            upload_photo_questions = UploadPhotoQuestionSerializer(
                obj.upload_photo_question_projects.filter(
                    main_task_number="task_3"
                ).order_by("sub_task_number")[:1],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            upload_photo_questions = UploadPhotoQuestionSerializer(
                obj.upload_photo_question_projects.filter(
                    is_active=1, main_task_number="task_3"
                ).order_by("sub_task_number")[:1],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            short_answers_questions = ShortAnswerQuestionSerializer(
                obj.short_question_projects.filter(main_task_number="task_3").order_by(
                    "sub_task_number"
                )[:1],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            short_answers_questions = ShortAnswerQuestionSerializer(
                obj.short_question_projects.filter(
                    is_active=1, main_task_number="task_3"
                ).order_by("sub_task_number")[:1],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            numeric_questions = NumericQuestionSerializer(
                obj.numeric_question_projects.filter(
                    main_task_number="task_3"
                ).order_by("sub_task_number")[:1],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            numeric_questions = NumericQuestionSerializer(
                obj.numeric_question_projects.filter(
                    is_active=1, main_task_number="task_3"
                ).order_by("sub_task_number")[:1],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            mcq_questions = MCQQuestionSerializer(
                obj.mcq_question_projects.filter(main_task_number="task_3").order_by(
                    "sub_task_number"
                )[:17],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            mcq_questions = MCQQuestionSerializer(
                obj.mcq_question_projects.filter(
                    is_active=1, main_task_number="task_3"
                ).order_by("sub_task_number")[:17],
                many=True,
                context={"request": self.context["request"]},
            ).data

        data = {
            "upload_photo_questions": upload_photo_questions,
            "short_answers_questions": short_answers_questions,
            "numeric_questions": numeric_questions,
            "mcq_questions": mcq_questions,
        }
        return data

    def get_task_4(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            short_answers_questions = ShortAnswerQuestionSerializer(
                obj.short_question_projects.filter(main_task_number="task_4").order_by(
                    "sub_task_number"
                )[:4],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            short_answers_questions = ShortAnswerQuestionSerializer(
                obj.short_question_projects.filter(
                    is_active=1, main_task_number="task_4"
                ).order_by("sub_task_number")[:4],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(main_task_number="task_4").order_by(
                    "sub_task_number"
                )[:7],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(
                    is_active=1, main_task_number="task_4"
                ).order_by("sub_task_number")[:7],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            upload_photo_questions = UploadPhotoQuestionSerializer(
                obj.upload_photo_question_projects.filter(
                    main_task_number="task_4"
                ).order_by("sub_task_number")[:4],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            upload_photo_questions = UploadPhotoQuestionSerializer(
                obj.upload_photo_question_projects.filter(
                    is_active=1, main_task_number="task_4"
                ).order_by("sub_task_number")[:4],
                many=True,
                context={"request": self.context["request"]},
            ).data

        data = {
            "upload_photo_questions": upload_photo_questions,
            "short_answers_questions": short_answers_questions,
            "essay_questions": essay_questions,
        }
        return data

    def get_task_5(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(main_task_number="task_5").order_by(
                    "sub_task_number"
                )[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(
                    is_active=1, main_task_number="task_5"
                ).order_by("sub_task_number")[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data

        return essay_questions

    def get_task_6(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(main_task_number="task_6").order_by(
                    "sub_task_number"
                )[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(
                    is_active=1, main_task_number="task_6"
                ).order_by("sub_task_number")[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data
        return essay_questions

    def get_task_7(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(main_task_number="task_7").order_by(
                    "sub_task_number"
                )[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(
                    is_active=1, main_task_number="task_7"
                ).order_by("sub_task_number")[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data

        return essay_questions

    def get_task_8(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(main_task_number="task_8").order_by(
                    "sub_task_number"
                )[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            essay_questions = EssayQuestionSerializer(
                obj.essay_question_projects.filter(
                    is_active=1, main_task_number="task_8"
                ).order_by("sub_task_number")[:5],
                many=True,
                context={"request": self.context["request"]},
            ).data

        return essay_questions

    def get_task_9(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            short_answers_questions = ShortAnswerQuestionSerializer(
                obj.short_question_projects.filter(main_task_number="task_9").order_by(
                    "sub_task_number"
                )[:2],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            short_answers_questions = ShortAnswerQuestionSerializer(
                obj.short_question_projects.filter(
                    is_active=1, main_task_number="task_9"
                ).order_by("sub_task_number")[:2],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            dropdown_questions = DropdownQuestionSerializer(
                obj.dropdown_question_projects.filter(
                    main_task_number="task_9"
                ).order_by("sub_task_number")[:2],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            dropdown_questions = DropdownQuestionSerializer(
                obj.dropdown_question_projects.filter(
                    is_active=1, main_task_number="task_9"
                ).order_by("sub_task_number")[:2],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            numeric_questions = NumericQuestionSerializer(
                obj.numeric_question_projects.filter(
                    main_task_number="task_9"
                ).order_by("sub_task_number")[:17],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            numeric_questions = NumericQuestionSerializer(
                obj.numeric_question_projects.filter(
                    is_active=1, main_task_number="task_9"
                ).order_by("sub_task_number")[:17],
                many=True,
                context={"request": self.context["request"]},
            ).data

        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            percentage_questions = PercentageQuestionSerializer(
                obj.percentage_question_projects.filter(
                    main_task_number="task_9"
                ).order_by("sub_task_number")[:4],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            percentage_questions = PercentageQuestionSerializer(
                obj.percentage_question_projects.filter(
                    is_active=1, main_task_number="task_9"
                ).order_by("sub_task_number")[:4],
                many=True,
                context={"request": self.context["request"]},
            ).data

        data = {
            "dropdown_questions": dropdown_questions,
            "short_answers_questions": short_answers_questions,
            "numeric_questions": numeric_questions,
            "percentage_questions": percentage_questions,
        }
        return data

    def get_task_10(self, obj):
        if (
                self.context["request"].user.user_type == "admin"
                or self.context["request"].user.user_type == "sub_admin"
        ):
            exit_test_questions = ExitTestQuestionSerializer(
                obj.exit_test_question_projects.filter(
                    main_task_number="task_10"
                ).order_by("sub_task_number")[:20],
                many=True,
                context={"request": self.context["request"]},
            ).data
        else:
            exit_test_questions = ExitTestQuestionSerializer(
                obj.exit_test_question_projects.filter(
                    is_active=1, main_task_number="task_10"
                ).order_by("sub_task_number")[:20],
                many=True,
                context={"request": self.context["request"]},
            ).data

        return exit_test_questions


class StudentFeedbackSerializer(serializers.ModelSerializer):
    project_title = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    student_membership_id = serializers.SerializerMethodField()

    class Meta:
        model = StudentFeedback
        fields = ["id", "project", "user", "project_title", "fullname", "student_membership_id", "feedback", "rating"]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get("user") or self.context.get("request").user
        validated_data["user"] = user
        return super().create(validated_data)

    def get_project_title(self, obj):
        try:
            return obj.project.title
        except:
            return ""

    def get_fullname(self, obj):
        try:
            return obj.user.fullname
        except:
            return ""

    def get_student_membership_id(self, obj):
        try:
            return obj.user.student_details.student_membership_id
        except:
            return ""


class SpecialPowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialPower
        fields = [
            "id",
            "project",
            "state",
            "college",
            "university",
            "degree",
            "batch",
            "is_active",
        ]
        extra_kwargs = {
            "project": {"required": True},
            "state": {"required": True},
            "college": {"required": True},
            "university": {"required": True},
            "degree": {"required": True},
            "batch": {"required": True},
        }
