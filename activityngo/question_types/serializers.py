from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from activityngo.question_types.models import (DropdownQuestion,
                                               DropdownQuestionOption,
                                               EssayQuestion, ExitTestQuestion,
                                               ExitTestQuestionOption,
                                               McqOption, MCQQuestion,
                                               NumericQuestion,
                                               PercentageQuestion,
                                               ShortAnswerQuestion,
                                               TaskInstructions,
                                               UploadPhotoQuestion,
                                               VideoQuestion)
from activityngo.student_project.models import VideoQuestionAnswers


# from activityngo.student_project import serializer


class VideoQuestionSerializer(serializers.ModelSerializer):
    is_submitted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VideoQuestion
        fields = (
            "id",
            "project",
            "main_task_number",
            "sub_task_number",
            "title",
            "video_url",
            # "title_max_limit",
            # "video_url_max_limit",
            "thumbnail",
            "is_submitted",
            "is_active",
            "is_delete",
        )
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "title": {"required": True},
            "video_url": {"required": True},
            # "title_max_limit": {"required": True},
            # "video_url_max_limit": {"required": True},
        }

    def get_is_submitted(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            # return obj.video_question_answers.filter(user=self.context["request"].user,order_details=self.context["order_details"],).exists()
            obj = VideoQuestionAnswers.objects.filter(
                question=obj,
                user=self.context["request"].user,
                order_details=self.context["order_details"],
            ).exists()
            return obj
        else:
            # For admin
            return False


class EssayQuestionSerializer(serializers.ModelSerializer):
    submitted_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EssayQuestion
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            # "answer": {"required": True},
            # "action_needed": {"required": True},
            # "characters_allowed_in_answer_box": {"required": True},
            "special_characters_in_answer_box": {"required": True},
            "grammar_check_in_answer_box": {"required": True},
            "answer_character_minimum_limit": {"required": True},
            "answer_character_maximum_limit": {"required": True},
            "copy_paste_answer_box": {"required": True},
        }

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.essay_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {"is_submitted": False, "answers": ""}
            if queryset:
                data["is_submitted"] = True
                data["answers"] = queryset.first().answer
            return data
        else:
            # For admin
            return False


class ShortAnswerQuestionSerializer(serializers.ModelSerializer):
    submitted_details = serializers.SerializerMethodField(read_only=True)
    question_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShortAnswerQuestion
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            "answer": {"required": True},
            # "action_needed": {"required": True},
            # "characters_allowed_in_answer_box": {"required": True},
            # "special_characters_in_answer_box": {"required": True},
            # "grammar_check_in_answer_box": {"required": True},
            "answer_character_minimum_limit": {"required": True},
            "answer_character_maximum_limit": {"required": True},
        }

    def get_question_type(self, obj):
        return "short_answers_questions"

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.short_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {"is_submitted": False, "answers": ""}
            if queryset:
                data["is_submitted"] = True
                data["answers"] = queryset.first().answer
            return data
        else:
            # For admin
            return False


class NumericQuestionSerializer(serializers.ModelSerializer):
    submitted_details = serializers.SerializerMethodField(read_only=True)
    question_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NumericQuestion
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            "answer": {"required": True},
            # "action_needed": {"required": True},
            # "characters_allowed_in_answer_box": {"required": True},
            # "no_of_digits_allowed": {"required": True},
            # "copy_paste_answer_box": {"required": True},
            "answer_character_minimum_limit": {"required": True},
            "answer_character_maximum_limit": {"required": True},
        }

    def get_question_type(self, obj):
        return "numeric_questions"

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.numeric_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {"is_submitted": False, "answers": ""}
            if queryset:
                data["is_submitted"] = True
                data["answers"] = queryset.first().answer
            return data
        else:
            # For admin
            return False


class PercentageQuestionSerializer(serializers.ModelSerializer):
    submitted_details = serializers.SerializerMethodField(read_only=True)
    question_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PercentageQuestion
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            "answer": {"required": True},
            # "action_needed": {"required": True},
            # "characters_allowed_in_answer_box": {"required": True},
            # "special_characters_in_answer": {"required": True},
            # "copy_paste_answer_box": {"required": True},
            "answer_character_minimum_limit": {"required": True},
            "answer_character_maximum_limit": {"required": True},
        }

    def get_question_type(self, obj):
        return "percentage_questions"

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.percentage_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {"is_submitted": False, "answers": ""}
            if queryset:
                data["is_submitted"] = True
                data["answers"] = queryset.first().answer
            return data
        else:
            # For admin
            return False


class MCQOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqOption
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "mcq_question": {"required": True},
            "option": {"required": True},
            "right_answer_option_among_multiple_choice": {"required": True},
        }


class MCQQuestionSerializer(serializers.ModelSerializer):
    options = serializers.ListSerializer(
        required=True, child=serializers.DictField(), write_only=True
    )
    submitted_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MCQQuestion
        # exclude = ['is_delete', 'update_time']
        fields = (
            "id",
            "project",
            "main_task_number",
            "sub_task_number",
            "question",
            "number_of_options",
            "question_character_maximum_limit",
            # "copy_paste_question_box",
            # "special_characters_in_questions",
            "minimum_number_of_options_in_mcq",
            "maximum_number_of_options_in_mcq",
            "mcq_options_character_maximum_limit",
            "copy_paste_answer_box",
            "special_characters_in_answer_box",
            "action_needed",
            "number_of_options_allowed_to_select_among_mcq",
            "is_active",
            "create_time",
            "options",
            "submitted_details",
        )
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            "number_of_options": {"required": True},
            "action_needed": {"required": True},
            # "minimum_number_of_options_in_mcq": {"required": True},
            # "maximum_number_of_options_in_mcq": {"required": True},
            # "mcq_options_character_maximum_limit": {"required": True},
            # "copy_paste_answer_box": {"required": True},
            # "special_characters_in_answer_box": {"required": True},
            # "number_of_options_allowed_to_select_among_mcq": {"required": True},
        }

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.mcq_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {
                "is_submitted": False,
                "answers": [],
                "mca_question_option": MCQOptionSerializer(
                    obj.mca_question_option.all(), many=True
                ).data,
            }
            if queryset:
                data["is_submitted"] = True
                # data['answers'] = serializer.AnswersMCQQuestionSerializer(
                #     queryset.first().mcq_selected_options.all(), many=True).data
            return data
        else:
            # For admin
            if "obj" in self.context.keys():
                obj = self.context["obj"]
            return MCQOptionSerializer(obj.mca_question_option.all(), many=True).data

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        if instance is None:  # validation while creating obj
            if int(attrs["number_of_options"]) != len(attrs["options"]):
                raise serializers.ValidationError(
                    _(f"Please add {attrs['number_of_options']} options.")
                )
        # else:
        #     if attrs['options']:
        #         if int(attrs['number_of_options']) != len(attrs['options']):
        #             raise serializers.ValidationError(_(f"Please add {attrs['number_of_options']} options."))
        return super().validate(attrs)

    def save(self, **kwargs):
        options = self.validated_data.pop("options", [])

        is_create = self.instance is None

        if is_create:
            # This is a create operation
            # You can perform create-specific logic here
            obj = super().create(self.validated_data)
            # super().save(**kwargs)  # Call the parent class save method to actually create the object
        else:
            # This is an update operation
            # You can perform update-specific logic here
            obj = super().save(**kwargs)

            # Add Options to McqOption Table
        for item in options:
            McqOption.objects.create(
                mcq_question=obj,
                option=item["option"],
                right_answer_option_among_multiple_choice=item["is_right_answers"],
            )
        self.context["obj"] = obj
        return obj


class UploadPhotoQuestionSerializer(serializers.ModelSerializer):
    submitted_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UploadPhotoQuestion
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            "answer": {"required": True},
            # "action_needed": {"required": True},
            "allowed_format": {"required": True},
            # "minimum_file_size_allowed": {"required": True},
            # "maximum_file_size_allowed": {"required": True},
        }

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.upload_photo_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {"is_submitted": False, "answers": ""}
            if queryset:
                data["is_submitted"] = True
                data["answers"] = queryset.first().answer.url
            return data
        else:
            # For admin
            return False


class ExitTestQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExitTestQuestionOption
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "exit_test_question": {"required": True},
            "option": {"required": True},
            "right_answer_option_among_multiple_choice": {"required": True},
        }


# class ExitSelectedOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExitSelectedOptions
#         fields = ['id', 'answer']


class ExitTestQuestionSerializer(serializers.ModelSerializer):
    options = serializers.ListSerializer(
        required=True, child=serializers.DictField(), write_only=True
    )
    submitted_details = serializers.SerializerMethodField(read_only=True)

    # exit_options = ExitSelectedOptionsSerializer(source="exit_selected_options", read_only=True, many=True)

    class Meta:
        model = ExitTestQuestion
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            "number_of_options": {"required": True},
            # "action_needed": {"required": True},
            # "minimum_number_of_options_in_mcq": {"required": True},
            # "maximum_number_of_options_in_mcq": {"required": True},
            # "mcq_options_character_maximum_limit": {"required": True},
            # "copy_paste_answer_box": {"required": True},
            # "special_characters_in_answer_box": {"required": True},
            "number_of_options_allowed_to_select_among_mcq": {"required": True},
        }

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.exit_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {
                "is_submitted": False,
                "answers": [],
                "exit_options": ExitTestQuestionOptionSerializer(
                    obj.exit_test_question_option.all(), many=True
                ).data,
            }
            if queryset:
                data["is_submitted"] = True
                data["answers"] = queryset.first().answer.option
            return data
        else:
            # For admin
            if "obj" in self.context.keys():
                obj = self.context["obj"]
            return ExitTestQuestionOptionSerializer(
                obj.exit_test_question_option.all(), many=True
            ).data

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        if instance is None:  # validation while creating obj
            if int(attrs["number_of_options"]) != len(attrs["options"]):
                # if int(attrs['number_of_options']) != len(attrs['options']):
                raise serializers.ValidationError(
                    _(f"Please add {attrs['number_of_options']} options.")
                )
        return super().validate(attrs)

    def save(self, **kwargs):
        options = self.validated_data.pop("options", [])
        # if self.context.get('request').method != 'PATCH':
        #     obj = super().create(self.validated_data)
        # else:
        #     obj = self.instance
        is_create = self.instance is None

        if is_create:
            # This is a create operation
            # You can perform create-specific logic here
            obj = super().create(self.validated_data)
            # super().save(**kwargs)  # Call the parent class save method to actually create the object
        else:
            # This is an update operation
            # You can perform update-specific logic here
            obj = super().save(**kwargs)
        # Add Options to ExitTestQuestionOption Table
        for item in options:
            ExitTestQuestionOption.objects.create(
                exit_test_question=obj,
                option=item["option"],
                right_answer_option_among_multiple_choice=item["is_right_answers"],
            )
        self.context["obj"] = obj
        return obj


class DropdownQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropdownQuestionOption
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "dropdown_question": {"required": True},
            "option": {"required": True},
            "right_answer_option_among_multiple_choice": {"required": True},
        }


# class DropDownSelectedOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DropDownSelectedOptions
#         fields = ['id', 'answer']


class DropdownQuestionSerializer(serializers.ModelSerializer):
    options = serializers.ListSerializer(
        required=True, child=serializers.DictField(), write_only=True
    )
    submitted_details = serializers.SerializerMethodField(read_only=True)
    question_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DropdownQuestion
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "question": {"required": True},
            "number_of_options": {"required": True},
            # "action_needed": {"required": True},
            # "number_of_dropdowns_in_mcq": {"required": True},
            # "copy_paste_answer_box": {"required": True},
            # "special_characters_in_answer_box": {"required": True},
        }

    def get_question_type(self, obj):
        return "dropdown_answers_questions"

    def get_submitted_details(self, obj):
        if "order_details" in self.context.keys():
            # For Student : In Exam
            queryset = obj.dropdown_question_answers.filter(
                user=self.context["request"].user,
                order_details=self.context["order_details"],
                survey_number=self.context["survey_number"],
            )
            data = {
                "is_submitted": False,
                "answers": [],
                "dropdown_question_option": DropdownQuestionOptionSerializer(
                    obj.dropdown_question_option.all(), read_only=True, many=True
                ).data,
            }
            if queryset:
                data["is_submitted"] = True

                # print(f"-->{DropDownSelectedOptionsSerializer(source="dropdown_selected_options", read_only=True,many=True)}<<---")

                # data["answers"] = DropDownSelectedOptionsSerializer(
                #     queryset.first().dropdown_selected_options.all(), many=True
                # ).data
                #
                data["answers"] = queryset.first().answer.option
            return data
        else:
            # For admin
            if "obj" in self.context.keys():
                obj = self.context["obj"]
            return DropdownQuestionOptionSerializer(
                obj.dropdown_question_option.all(), many=True
            ).data

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        if instance is None:  # validation while creating obj
            if int(attrs["number_of_options"]) != len(attrs["options"]):
                # if int(attrs['number_of_options']) != len(attrs['options']):
                raise serializers.ValidationError(
                    _(f"Please add {attrs['number_of_options']} options.")
                )
        return super().validate(attrs)

    def save(self, **kwargs):
        options = self.validated_data.pop("options", [])
        is_create = self.instance is None

        if is_create:
            # This is a create operation
            # You can perform create-specific logic here
            obj = super().create(self.validated_data)
            # super().save(**kwargs)  # Call the parent class save method to actually create the object
        else:
            # This is an update operation
            # You can perform update-specific logic here
            obj = super().save(**kwargs)

        # Add Options to DropdownQuestionOption Table
        for item in options:
            DropdownQuestionOption.objects.create(
                dropdown_question=obj,
                option=item["option"],
                right_answer_option_among_multiple_choice=item["is_right_answers"],
            )
        self.context["obj"] = obj
        return obj


class TaskInstructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstructions
        exclude = ["is_delete", "update_time"]
        extra_kwargs = {
            "project": {"required": True},
            "main_task_number": {"required": True},
            "sub_task_number": {"required": True},
            "task_instructions": {"required": True},
            # "instructions_character_maximum_limit": {"required": True},
            # "action_needed": {"required": True},
            # "copy_paste_option_in_instruction_box": {"required": True},
            # "special_characters_in_instruction_box": {"required": True},
            # "image_in_instruction_box": {"required": True},
            # "url_in_instruction_box": {"required": True},
            "task_name": {"required": True},
            # "task_completed_hours": {"required": True},
            "number_of_surveys": {"required": True},
        }


class TaskInstructionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstructions
        exclude = ["is_delete", "update_time"]
