from rest_framework import serializers

MODEL_NAME = (
    ("essay_question", "EssayQuestionAnswers"),
    ("upload_photo_question", "UploadPhotoQuestionAnswers"),
    ("short_question", "ShortQuestionAnswers"),
    ("numeric_question", "NumericQuestionAnswers"),
    ("dropdown_question", "DropDownQuestionAnswers"),
    ("percentage_question", "PercentageQuestionAnswers"),
    ("mcq_question", "MCQQuestionAnswers"),
    ("exit_question", "ExitQuestionAnswers"),
)


class DynamicQuestionDetailsSerializer(serializers.Serializer):
    model_name = serializers.ChoiceField(choices=MODEL_NAME, required=True)
    question_id = serializers.IntegerField(required=True)


class DynamicRejectedQuestionSerializer(serializers.Serializer):
    reject_data = serializers.ListField(
        child=DynamicQuestionDetailsSerializer(required=True),
        required=True,
        min_length=1,
    )

    def validate(self, data):
        # Retrieve the list of question details
        question_details_list = data.get("reject_data", [])

        # Create a set to store unique combinations of model_name and question_id
        unique_combinations = set()

        # Check for uniqueness within the list
        for question_details in question_details_list:
            model_name = question_details["model_name"]
            question_id = question_details["question_id"]
            combination = (model_name, question_id)

            if combination in unique_combinations:
                raise serializers.ValidationError(
                    "Each combination of model_name and question_id must be unique."
                )

            unique_combinations.add(combination)

        return data


def dynamic_question_answer_serializer(model_name):
    # Define a serializer class dynamically
    class DynamicSerializer(serializers.ModelSerializer):
        question = serializers.SerializerMethodField()
        question_id = serializers.SerializerMethodField()
        question_type = serializers.SerializerMethodField()
        answer = serializers.SerializerMethodField()
        answer_option = serializers.SerializerMethodField()
        answer_validation = serializers.SerializerMethodField()

        class Meta:
            model = model_name  # Set the model dynamically
            fields = (
                "id",
                "question_id",
                "question",
                "question_type",
                "answer_validation",
                "user",
                "status",
                "answer_option",
                "answer",
                "order_details",
                "survey_number",
                "reject_reason",
            )

        def get_answer_validation(self, obj):
            try:
                current_model_name = obj.question._meta.object_name

                question_set_1 = [
                    "EssayQuestion",
                    "ShortAnswerQuestion",
                    "PercentageQuestion",
                    "NumericQuestion",
                ]
                question_set_2 = ["MCQQuestion", "ExitTestQuestion", "DropdownQuestion"]
                question_set_3 = ["UploadPhotoQuestion"]

                validation_dict = {}
                if current_model_name in question_set_1:
                    validation_dict.update(
                        {
                            "action_needed": obj.question.action_needed,
                            "characters_allowed_in_answer_box": obj.question.characters_allowed_in_answer_box,
                            "special_characters_in_answer_box": obj.question.special_characters_in_answer_box,
                            "answer_character_minimum_limit": obj.question.answer_character_minimum_limit,
                            "answer_character_maximum_limit": obj.question.answer_character_maximum_limit,
                            "copy_paste_answer_box": obj.question.copy_paste_answer_box,
                        }
                    )
                    if current_model_name == 'EssayQuestion' or current_model_name == 'ShortAnswerQuestion':
                        validation_dict.update(
                            {
                                "grammar_check_in_answer_box": obj.question.grammar_check_in_answer_box,
                            }
                        )


                elif current_model_name in question_set_2:
                    validation_dict.update(
                        {
                            "action_needed": obj.question.action_needed,
                            "copy_paste_answer_box": obj.question.copy_paste_answer_box,
                            "special_characters_in_answer_box": obj.question.special_characters_in_answer_box,
                        }
                    )

                elif current_model_name in question_set_3:
                    validation_dict.update(
                        {
                            "action_needed": obj.question.action_needed,
                            "allowed_format": obj.question.allowed_format,
                            "minimum_file_size_allowed": obj.question.minimum_file_size_allowed,
                            "maximum_file_size_allowed": obj.question.maximum_file_size_allowed,
                        }
                    )

                return validation_dict if validation_dict else None
            except:
                return None

        def get_question_id(self, obj):
            try:
                return obj.question.id
            except:
                return ""

        def get_answer(self, obj):
            try:
                choice_type_question = [
                    "MCQQuestion",
                    "ExitTestQuestion",
                    "DropdownQuestion",
                ]
                url_models = ["UploadPhotoQuestion"]
                current_model_name = obj.question._meta.object_name
                if current_model_name in choice_type_question:
                    return obj.answer.option
                elif current_model_name in url_models:
                    return obj.answer.url
                return obj.answer
            except:
                return ""

        def get_answer_option(self, obj):
            try:
                choice_type_question = {
                    "MCQQuestion": "mca_question_option",
                    "ExitTestQuestion": "exit_test_question_option",
                    "DropdownQuestion": "dropdown_question_option",
                }
                current_model_name = obj.question._meta.object_name

                if choice_type_question.get(current_model_name):
                    related_field_name = choice_type_question[current_model_name]
                    related_field = getattr(obj.question, related_field_name)

                    if choice_type_question.get(current_model_name) == "MCQQuestion":
                        return related_field.all().values_list("id", "option")

                    related_field_values = [
                        {"id": item["id"], "is_active": item["is_active"], "create_time": item["create_time"],
                         "option": item["option"],
                         "right_answer_option_among_multiple_choice": item["right_answer_option_among_multiple_choice"]}
                        for item in
                        related_field.all().values("id", "is_active", "create_time", "option",
                                                   "right_answer_option_among_multiple_choice")]
                    return related_field_values

                return [{"id": None, "is_active": None, "create_time": None, "option": None,
                         "right_answer_option_among_multiple_choice": None, }]
            except Exception as e:
                return [{"id": None, "is_active": None, "create_time": None, "option": None,
                         "right_answer_option_among_multiple_choice": None, }]

        def get_question(self, obj):
            try:
                return obj.question.question
            except:
                return ""

        def get_answer_max_length(self, obj):
            try:
                return obj.question.answer_character_maximum_limit
            except:
                return ""

        def get_answer_min_length(self, obj):
            try:
                return obj.question.answer_character_minimum_limit
            except:
                return ""

        def get_question_type(self, obj):
            try:
                return model_name.__name__
            except:
                return ""

    return DynamicSerializer


# class DynamicTask3RejectedQuestionSerializer(serializers.Serializer):
#     question_id = serializers.IntegerField(required=True)
#     survey_number = serializers.ListField(child=serializers.IntegerField(),
#                                           min_length=1
#                                           )
