from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from django.utils import timezone
from activityngo.custom_auth.models import ApplicationUser, BaseModel
from activityngo.order.models import OrderDetail
from activityngo.question_types.models import (DropdownQuestion,
                                               DropdownQuestionOption,
                                               EssayQuestion, ExitTestQuestion,
                                               ExitTestQuestionOption,
                                               McqOption, MCQQuestion,
                                               NumericQuestion,
                                               PercentageQuestion,
                                               ShortAnswerQuestion,
                                               UploadPhotoQuestion,
                                               VideoQuestion)
from activityngo.utils.utils import get_upload_photo_question_path

ANSWERS_STATUS = (
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
    ("Submitted", "Submitted"),
)


class VideoQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        VideoQuestion, on_delete=models.CASCADE, related_name="video_question_answers"
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="video_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="video_question_order_details",
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Video Question Answers")
        verbose_name_plural = _("Video Questions Answers")
        unique_together = ("question", "user", "order_details")


class EssayQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        EssayQuestion, on_delete=models.CASCADE, related_name="essay_question_answers"
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="essay_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.CharField(_("Answer"), max_length=1024, null=True, blank=True)
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="essay_question_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Essay Question Answers")
        verbose_name_plural = _("Essay Questions Answers")
        # unique_together = ('question', 'user', 'order_details', 'survey_number')


class UploadPhotoQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        UploadPhotoQuestion,
        on_delete=models.CASCADE,
        related_name="upload_photo_question_answers",
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="upload_photo_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.ImageField(_("Answer"), upload_to=get_upload_photo_question_path)
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="upload_photo_question_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Upload Photo Question Answers")
        verbose_name_plural = _("Upload Photo Questions Answers")
        # unique_together = ('question', 'user', "order_details", 'survey_number')


class ShortQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        ShortAnswerQuestion,
        on_delete=models.CASCADE,
        related_name="short_question_answers",
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="short_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.CharField(_("Answer"), max_length=512, null=True, blank=True)
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="short_question_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Short Question Answers")
        verbose_name_plural = _("Short Questions Answers")
        # unique_together = ('question', 'user', "order_details", 'survey_number')


class NumericQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        NumericQuestion,
        on_delete=models.CASCADE,
        related_name="numeric_question_answers",
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="numeric_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.FloatField(_("Answer"), max_length=512, null=True, blank=True)
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="numeric_question_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Numeric Question Answers")
        verbose_name_plural = _("Numeric Questions Answers")
        # unique_together = ('question', 'user', "order_details", 'survey_number')


class DropDownQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        DropdownQuestion,
        on_delete=models.CASCADE,
        related_name="dropdown_question_answers",
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="dropdown_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.ForeignKey(
        DropdownQuestionOption,
        on_delete=models.CASCADE,
        related_name="dropdown_question_answers",
        null=True,
    )
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="dropdown_question_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("DropDown Question Answers")
        verbose_name_plural = _("DropDown Questions Answers")
        # unique_together = ('question', 'user', "order_details", 'survey_number')


# class DropDownSelectedOptions(BaseModel):
#     question_answers = models.ForeignKey(DropDownQuestionAnswers, on_delete=models.CASCADE,
#                                          related_name="dropdown_selected_options")
#     answer = models.CharField(_('Answer'), max_length=512, null=True, blank=True)


class PercentageQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        PercentageQuestion,
        on_delete=models.CASCADE,
        related_name="percentage_question_answers",
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="percentage_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.FloatField(_("Answer"), max_length=512, null=True, blank=True)
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="percentage_question_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Percentage Question Answers")
        verbose_name_plural = _("Percentage Questions Answers")
        # unique_together = ('question', 'user', "order_details", 'survey_number')


class MCQQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        MCQQuestion, on_delete=models.CASCADE, related_name="mcq_question_answers"
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="mcq_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.ForeignKey(
        McqOption,
        on_delete=models.CASCADE,
        related_name="mcq_question_answers",
        null=True,
    )
    order_details = models.ForeignKey(
        OrderDetail, on_delete=models.CASCADE, related_name="mcq_question_order_details"
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("MCQ Question Answers")
        verbose_name_plural = _("MCQ Questions Answers")
        # unique_together = ('question', 'user', "order_details", 'survey_number')


# class MCQSelectedOptions(BaseModel):
#     question_answers = models.ForeignKey(MCQQuestionAnswers, on_delete=models.CASCADE,
#                                          related_name="mcq_selected_options")
#     answer = models.CharField(_('Answer'), max_length=512, null=True, blank=True)


class ExitQuestionAnswers(BaseModel):
    question = models.ForeignKey(
        ExitTestQuestion, on_delete=models.CASCADE, related_name="exit_question_answers"
    )
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="exit_question_answers_user",
    )
    status = models.CharField(_("Status"), max_length=10, choices=ANSWERS_STATUS)
    answer = models.ForeignKey(
        ExitTestQuestionOption,
        on_delete=models.CASCADE,
        related_name="exit_question_answers",
        null=True,
    )
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="exit_question_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    reject_reason = models.CharField(
        _("Reject Reason"), max_length=256, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Exit Question Answers")
        verbose_name_plural = _("Exit Questions Answers")
        # unique_together = ('question', 'user', "order_details", 'survey_number')


# class ExitSelectedOptions(BaseModel):
#     question_answers = models.ForeignKey(ExitQuestionAnswers, on_delete=models.CASCADE,
#                                          related_name="exit_selected_options")
#     answer = models.CharField(_('Answer'), max_length=512, null=True, blank=True)


# Task 3 Complete all surveys details
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


class SurveysDetails(BaseModel):
    user = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="task3_surveys_details_user",
    )
    order_details = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="task3_surveys_details_order_details",
    )
    survey_number = models.IntegerField(
        _("Survey Form Number"), validators=[MinValueValidator(1)], default=1
    )
    main_task_number = models.CharField(
        _("Main task number"), max_length=10, choices=MAIN_TASK_NUMBER
    )

    class Meta:
        verbose_name = _("Surveys Details")
        verbose_name_plural = _("Surveys Details")
        # unique_together = ('user', "order_details", 'survey_number', 'main_task_number')


class StudentTaskStatus(BaseModel):
    TASK_STATUS = Choices(
        ("not_submitted", "Not Submitted"),
        ("answer_rejected_in_evaluation", "Answer Rejected in Evaluation"),
        ("submitted_for_evaluation", "Submitted for Evaluation"),
        ("all_answers_are_accepted", "All answers are accepted"),
        ("not_applicable", "Not Applicable"),
        ("task_3_photo_rejected", "Task 3 photo rejected"),
    )
    order_details = models.OneToOneField(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name="student_task_status_order_details",
    )
    task1 = models.CharField(
        _("Task 1"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task2 = models.CharField(
        _("Task 2"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )

    task3 = models.CharField(
        _("Task 3"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task3_submissions = models.PositiveIntegerField(
        (_("task 3 submissions")), default=0
    )
    task4 = models.CharField(
        _("Task 4"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task5 = models.CharField(
        _("Task 5"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task6 = models.CharField(
        _("Task 6"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task7 = models.CharField(
        _("Task 7"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task8 = models.CharField(
        _("Task 8"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task9 = models.CharField(
        _("Task 9"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    task10 = models.CharField(
        _("Task 10"),
        max_length=30,
        choices=TASK_STATUS,
        default=TASK_STATUS.not_applicable,
        null=True,
        blank=True,
    )
    submit_time_task_1 = models.DateTimeField(
        _("submit time task 1"), null=True, blank=True
    )
    submit_time_task_2 = models.DateTimeField(
        _("submit time task 2"), null=True, blank=True
    )
    submit_time_task_3 = models.DateTimeField(
        _("submit time task 3"), null=True, blank=True
    )
    submit_time_task_4 = models.DateTimeField(
        _("submit time task 4"), null=True, blank=True
    )
    submit_time_task_5 = models.DateTimeField(
        _("submit time task 5"), null=True, blank=True
    )
    submit_time_task_6 = models.DateTimeField(
        _("submit time task 6"), null=True, blank=True
    )
    submit_time_task_7 = models.DateTimeField(
        _("submit time task 7"), null=True, blank=True
    )
    submit_time_task_8 = models.DateTimeField(
        _("submit time task 8"), null=True, blank=True
    )
    submit_time_task_9 = models.DateTimeField(
        _("submit time task 9"), null=True, blank=True
    )
    submit_time_task_10 = models.DateTimeField(
        _("submit time task 10"), null=True, blank=True
    )

    def save(self, *args, **kwargs):
        number_of_points = self.order_details.number_of_points
        tasks = [getattr(self, f"task{i}") for i in range(1, 11)]

        points_to_tasks = {
            "points_05": 4,
            "points_10": 6,
            "points_20": 10
        }

        max_tasks_to_check = points_to_tasks.get(number_of_points)

        if max_tasks_to_check is not None and all(
                task == "all_answers_are_accepted" for task in tasks[:max_tasks_to_check]
        ):
            order = self.order_details
            order.is_complete = True
            order.activity_completed_date = timezone.now()
            order.activity_completed_date_by_student = timezone.now()
            order.save()

        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     number_of_points = self.order_details.number_of_points
    #     tasks = [getattr(self, f"task{i}") for i in range(1, 11)]
    #
    #     if number_of_points == "points_05" and all(
    #         task == "all_answers_are_accepted" for task in tasks[:4]
    #     ):
    #         order = self.order_details
    #         order.is_complete = True
    #         order.activity_completed_date = timezone.now()
    #         order.activity_completed_date_by_student = timezone.now()
    #         order.save()
    #     elif number_of_points == "points_10" and all(
    #         task == "all_answers_are_accepted" for task in tasks[:6]
    #     ):
    #         order = self.order_details
    #         order.is_complete = True
    #         order.activity_completed_date = timezone.now()
    #         order.activity_completed_date_by_student = timezone.now()
    #         order.save()
    #     elif number_of_points == "points_20" and all(
    #         task == "all_answers_are_accepted" for task in tasks
    #     ):
    #         order = self.order_details
    #         order.is_complete = True
    #         order.activity_completed_date = timezone.now()
    #         order.activity_completed_date_by_student = timezone.now()
    #         order.save()
    #
    #     super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if (
    #             self.order_details.number_of_points == "points_05" and
    #             self.task1 == "all_answers_are_accepted" and
    #             self.task2 == "all_answers_are_accepted" and
    #             self.task3 == "all_answers_are_accepted" and
    #             self.task4 == "all_answers_are_accepted"
    #     ) or (self.order_details.number_of_points == "points_10" and
    #           self.task1 == "all_answers_are_accepted" and
    #           self.task2 == "all_answers_are_accepted" and
    #           self.task3 == "all_answers_are_accepted" and
    #           self.task4 == "all_answers_are_accepted" and
    #           self.task5 == "all_answers_are_accepted" and
    #           self.task6 == "all_answers_are_accepted"
    #     ) or (self.order_details.number_of_points == "points_20" and
    #           self.task1 == "all_answers_are_accepted" and
    #           self.task2 == "all_answers_are_accepted" and
    #           self.task3 == "all_answers_are_accepted" and
    #           self.task4 == "all_answers_are_accepted" and
    #           self.task5 == "all_answers_are_accepted" and
    #           self.task6 == "all_answers_are_accepted" and
    #           self.task7 == "all_answers_are_accepted" and
    #           self.task8 == "all_answers_are_accepted" and
    #           self.task9 == "all_answers_are_accepted" and
    #           self.task10 == "all_answers_are_accepted"):
    #         order = self.order_details
    #         order.is_complete = True
    #         order.save()
    #
    #     elif (
    #             self.order_details.number_of_points == "points_10" and
    #             self.task1 == "all_answers_are_accepted" and
    #             self.task2 == "all_answers_are_accepted" and
    #             self.task3 == "all_answers_are_accepted" and
    #             self.task4 == "all_answers_are_accepted" and
    #             self.task5 == "all_answers_are_accepted" and
    #             self.task6 == "all_answers_are_accepted" and
    #             self.task7 == "all_answers_are_accepted" and
    #             self.task8 == "all_answers_are_accepted" and
    #             self.task9 == "all_answers_are_accepted" and
    #             self.task10 == "all_answers_are_accepted"
    #     ):
    #         order = self.order_details
    #         order.is_complete = True
    #         order.save()
    #
    #     super().save(*args, **kwargs)
