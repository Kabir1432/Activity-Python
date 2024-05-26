from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from multiselectfield import MultiSelectField

from activityngo.custom_auth.models import BaseModel
from activityngo.project.models import Project
from activityngo.utils.utils import get_upload_thumbnail_video_question_path

MAIN_TASK_NUMBER = Choices(
    ("task_1", "Task – 1"),
    ("task_2", "Task – 2"),
    ("task_3", "Task – 3"),
    ("task_4", "Task – 4"),
    ("task_5", "Task – 5"),
    ("task_6", "Task – 6"),
    ("task_7", "Task – 7"),
    ("task_8", "Task – 8"),
    ("task_9", "Task – 9"),
    ("task_10", "Task – 10"),
)


# Create your models here.
class VideoQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="video_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"),
        null=True,
        max_length=10,
        choices=MAIN_TASK_NUMBER,
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    title = models.CharField(_("Video Title"), max_length=512)
    video_url = models.URLField(_("Video URL"), max_length=512)
    # title_max_limit = models.PositiveIntegerField(
    #     _("Video Title Maximum Limit"),
    # )
    # video_url_max_limit = models.PositiveIntegerField(
    #     _("Video URL Maximum Limit"),
    # )
    thumbnail = models.ImageField(
        _("Thumbnail"),
        null=True,
        blank=True,
        upload_to=get_upload_thumbnail_video_question_path,
    )

    class Meta:
        verbose_name = _("Video Question")
        verbose_name_plural = _("Video Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class EssayQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="essay_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"),
        null=True,
        max_length=10,
        choices=MAIN_TASK_NUMBER,
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512, null=True)
    answer = models.CharField(_("Answer"), max_length=512, null=True)
    question_character_maximum_limit = models.CharField(
        _("Question Character Maximum Limit"), max_length=512, null=True, blank=True
    )
    copy_paste_question_box = models.BooleanField(
        _("Copy – Paste option in Question box"), default=True
    )
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed"), max_length=512, null=True, blank=True
    )
    characters_allowed_in_answer_box = models.CharField(
        _("Characters allowed in Answer Box"), max_length=512, null=True, blank=True
    )
    special_characters_in_answer_box = models.BooleanField(
        _("Special Characters in Answer Box"), null=True, blank=True
    )
    grammar_check_in_answer_box = models.BooleanField(
        _("Grammar Check in Answer Box"), null=True, blank=True
    )
    answer_character_minimum_limit = models.IntegerField(
        _("Answer Character Minimum Limit"), null=True, blank=True
    )
    answer_character_maximum_limit = models.IntegerField(
        _("Answer Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_answer_box = models.BooleanField(
        _("Copy – Paste option in Answer box"), default=True
    )

    class Meta:
        verbose_name = _("Essay Question")
        verbose_name_plural = _("Essay Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class ShortAnswerQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="short_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"),
        null=True,
        max_length=10,
        choices=MAIN_TASK_NUMBER,
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512, null=True)
    answer = models.CharField(_("Answer"), max_length=512, null=True)
    question_character_maximum_limit = models.CharField(
        _("Question Character Maximum Limit"), max_length=512, null=True, blank=True
    )
    copy_paste_question_box = models.BooleanField(
        _("Copy – Paste option in Question box"), default=True
    )
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed by Student"), max_length=512, null=True, blank=True
    )
    characters_allowed_in_answer_box = models.CharField(
        _("Characters allowed in Answer Box"), max_length=512, null=True, blank=True
    )
    special_characters_in_answer_box = models.BooleanField(
        _("Special Characters in Answer Box"), default=True
    )
    grammar_check_in_answer_box = models.BooleanField(
        _("Grammar Check in Answer Box"), default=True
    )
    answer_character_minimum_limit = models.IntegerField(
        _("Answer Character Minimum Limit"), null=True, blank=True
    )
    answer_character_maximum_limit = models.IntegerField(
        _("Answer Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_answer_box = models.BooleanField(
        _("Copy – Paste option in Answer box"), default=True
    )

    class Meta:
        verbose_name = _("Short Question")
        verbose_name_plural = _("Short Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class NumericQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="numeric_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"),
        null=True,
        max_length=10,
        choices=MAIN_TASK_NUMBER,
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512)
    answer = models.CharField(_("Answer"), max_length=512)
    question_character_maximum_limit = models.CharField(
        _("Question Character Maximum Limit"), max_length=512, null=True, blank=True
    )
    copy_paste_question_box = models.BooleanField(
        _("Copy – Paste option in Question box"), default=True
    )
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed by Student"), max_length=512, null=True, blank=True
    )
    characters_allowed_in_answer_box = models.IntegerField(
        _("Characters allowed in Answer Box"), null=True, blank=True
    )
    no_of_digits_allowed = models.IntegerField(
        _("No. of Digits allowed"), null=True, blank=True
    )
    copy_paste_answer_box = models.BooleanField(
        _("Copy – Paste option in Answer box"), default=True
    )
    answer_character_minimum_limit = models.IntegerField(
        _("Answer Character Minimum Limit"), null=True, blank=True
    )
    answer_character_maximum_limit = models.IntegerField(
        _("Answer Character Maximum Limit"), null=True, blank=True
    )
    special_characters_in_answer_box = models.BooleanField(
        _("Special Characters in Answer Box"), default=True
    )

    class Meta:
        verbose_name = _("Numeric Question")
        verbose_name_plural = _("Numeric Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class PercentageQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="percentage_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"),
        null=True,
        max_length=10,
        choices=MAIN_TASK_NUMBER,
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512)
    answer = models.CharField(_("Answer"), max_length=512)
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed by Student"), max_length=512, null=True, blank=True
    )
    characters_allowed_in_answer_box = models.IntegerField(
        _("Characters allowed in Answer Box"), null=True, blank=True
    )
    special_characters_in_answer_box = models.BooleanField(
        _("Special Characters in Answer Box"), default=True
    )
    copy_paste_answer_box = models.BooleanField(
        _("Copy – Paste option in Answer box"), default=True
    )
    answer_character_minimum_limit = models.IntegerField(
        _("Answer Character Minimum Limit"), null=True, blank=True
    )
    answer_character_maximum_limit = models.IntegerField(
        _("Answer Character Maximum Limit"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Percentage Question")
        verbose_name_plural = _("Percentage Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class MCQQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="mcq_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"), null=True, max_length=10, choices=MAIN_TASK_NUMBER
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512)
    number_of_options = models.IntegerField(
        _("Number of Options"), null=True, blank=True
    )
    question_character_maximum_limit = models.IntegerField(
        _("Question Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_question_box = models.BooleanField(
        _("Copy – Paste option in Question box"), default=True
    )
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    minimum_number_of_options_in_mcq = models.IntegerField(
        _("Minimum Number of Options in MCQ"), null=True, blank=True
    )
    maximum_number_of_options_in_mcq = models.IntegerField(
        _("Maximum Number of Options in MCQ"), null=True, blank=True
    )
    mcq_options_character_maximum_limit = models.IntegerField(
        _("MCQ Options Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_answer_box = models.BooleanField(
        _("Copy – Paste option in Answer box"), default=True
    )
    special_characters_in_answer_box = models.BooleanField(
        _("Special Characters in MCQ Option box"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed by Student"), max_length=512, null=True, blank=True
    )
    number_of_options_allowed_to_select_among_mcq = models.IntegerField(
        _("Number of Options allowed to select among MCQ"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("MCQ Question")
        verbose_name_plural = _("MCQ Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class McqOption(BaseModel):
    mcq_question = models.ForeignKey(
        MCQQuestion,
        on_delete=models.CASCADE,
        null=True,
        related_name="mca_question_option",
    )
    option = models.CharField(_("Option"), max_length=512)
    right_answer_option_among_multiple_choice = models.BooleanField(
        _("right_answer_option_among_multiple_choice"), default=False
    )

    class Meta:
        verbose_name = _("MCQ Option")
        verbose_name_plural = _("MCQ Option")


class UploadPhotoQuestion(BaseModel):
    ALLOWED_FORMAT = Choices(
        ("jpeg", "JPEG"),
        ("jpg", "JPG"),
        ("png", "PNG"),
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="upload_photo_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"),
        null=True,
        max_length=10,
        choices=MAIN_TASK_NUMBER,
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512)
    answer = models.CharField(_("Answer"), max_length=512)
    question_character_maximum_limit = models.IntegerField(
        _("Question Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_question_box = models.BooleanField(
        _("Copy – Paste option in Question box"), default=True
    )
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed by Student"), max_length=512, null=True, blank=True
    )
    allowed_format = MultiSelectField(
        _("Allowed Format"),
        choices=ALLOWED_FORMAT,
        max_length=255,
        null=True,
        blank=True,
    )
    minimum_file_size_allowed = models.IntegerField(
        _("Minimum File Size allowed"), null=True, blank=True
    )
    maximum_file_size_allowed = models.IntegerField(
        _("Maximum File Size allowed"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Upload Photo Question")
        verbose_name_plural = _("Upload Photo Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class ExitTestQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="exit_test_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"), null=True, max_length=10, choices=MAIN_TASK_NUMBER
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512)
    number_of_options = models.IntegerField(
        _("Number of Options"), null=True, blank=True
    )
    question_character_maximum_limit = models.IntegerField(
        _("Question Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_question_box = models.BooleanField(
        _("Copy – Paste option in Question box"), default=True
    )
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    minimum_number_of_options_in_mcq = models.IntegerField(
        _("Minimum Number of Options in MCQ"), null=True, blank=True
    )
    maximum_number_of_options_in_mcq = models.IntegerField(
        _("Maximum Number of Options in MCQ"), null=True, blank=True
    )
    mcq_options_character_maximum_limit = models.IntegerField(
        _("MCQ Options Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_answer_box = models.BooleanField(
        _("Copy – Paste option in Answer box"), default=True
    )
    special_characters_in_answer_box = models.BooleanField(
        _("Special Characters in MCQ Option box"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed by Student"), max_length=512, null=True, blank=True
    )
    number_of_options_allowed_to_select_among_mcq = models.IntegerField(
        _("Number of Options allowed to select among MCQ"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Exit Test Question")
        verbose_name_plural = _("Exit Test Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class ExitTestQuestionOption(BaseModel):
    exit_test_question = models.ForeignKey(
        ExitTestQuestion,
        on_delete=models.CASCADE,
        null=True,
        related_name="exit_test_question_option",
    )
    option = models.CharField(_("Option"), max_length=512)
    right_answer_option_among_multiple_choice = models.BooleanField(
        _("right_answer_option_among_multiple_choice"), default=False
    )

    class Meta:
        verbose_name = _("Exit Test Question Option")
        verbose_name_plural = _("Exit Test Questions Option")


class DropdownQuestion(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="dropdown_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"), null=True, max_length=10, choices=MAIN_TASK_NUMBER
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    question = models.CharField(_("Question"), max_length=512)
    number_of_options = models.IntegerField(
        _("Number of Options"), null=True, blank=True
    )
    question_character_maximum_limit = models.IntegerField(
        _("Question Character Maximum Limit"), null=True, blank=True
    )
    copy_paste_question_box = models.BooleanField(
        _("Copy – Paste option in Question box"), null=True, blank=True
    )
    special_characters_in_questions = models.BooleanField(
        _("Special Characters in Questions"), default=True
    )
    number_of_dropdowns_in_mcq = models.IntegerField(
        _("Number of Dropdowns in MCQ"), null=True, blank=True
    )
    copy_paste_answer_box = models.BooleanField(
        _("Copy – Paste option in Answer box"), default=True
    )
    special_characters_in_answer_box = models.BooleanField(
        _("Special Characters in MCQ Option box"), default=True
    )
    action_needed = models.CharField(
        _("Action Needed by Student"), max_length=512, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Dropdown Question")
        verbose_name_plural = _("Dropdown Questions")
        unique_together = ("project", "main_task_number", "sub_task_number")


class DropdownQuestionOption(BaseModel):
    dropdown_question = models.ForeignKey(
        DropdownQuestion,
        on_delete=models.CASCADE,
        null=True,
        related_name="dropdown_question_option",
    )
    option = models.CharField(_("Option"), max_length=512)
    right_answer_option_among_multiple_choice = models.BooleanField(
        _("right_answer_option_among_multiple_choice"), default=False
    )

    class Meta:
        verbose_name = _("Dropdown Question Option")
        verbose_name_plural = _("Dropdown Questions Option")


class TaskInstructions(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="task_instructions_question_projects",
    )
    main_task_number = models.CharField(
        _("Main task number"),
        null=True,
        max_length=10,
        choices=MAIN_TASK_NUMBER,
    )
    sub_task_number = models.PositiveIntegerField(_("Sub task number"), null=True)
    task_instructions = models.CharField(
        _("Task Instructions"), max_length=512, null=True, blank=True
    )
    # instructions_character_maximum_limit = models.IntegerField(
    #     _("Instructions Character Maximum Limit:"), null=True, blank=True
    # )
    # copy_paste_option_in_instruction_box = models.BooleanField(
    #     _("Copy – Paste option in Instruction box"), default=True
    # )
    # special_characters_in_instruction_box = models.BooleanField(
    #     _("Special Characters in Instruction box"), default=True
    # )
    # image_in_instruction_box = models.BooleanField(
    #     _("Image in Instruction box"), default=True
    # )
    # url_in_instruction_box = models.BooleanField(
    #     _("URL in Instruction box"), default=True
    # )
    # action_needed = models.CharField(
    #     _("Action Needed by Student"), max_length=512, null=True, blank=True
    # )
    task_name = models.CharField(_("Task Name"), max_length=512, null=True, blank=True)
    task_completed_hours = models.IntegerField(
        _("Total hours for task completed"),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Task Instructions")
        verbose_name_plural = _("Task Instructions")
        unique_together = ("project", "main_task_number", "sub_task_number")
