from django.contrib import admin

from activityngo.order.models import OrderDetail
from activityngo.student_project.models import (DropDownQuestionAnswers,
                                                EssayQuestionAnswers,
                                                ExitQuestionAnswers,
                                                MCQQuestionAnswers,
                                                NumericQuestionAnswers,
                                                PercentageQuestionAnswers,
                                                ShortQuestionAnswers,
                                                StudentTaskStatus,
                                                UploadPhotoQuestionAnswers,
                                                VideoQuestionAnswers)


# Register your models here.
class StudentTaskStatusInline(admin.TabularInline):
    model = StudentTaskStatus
    extra = 1


class VideoQuestionAnswersInline(admin.TabularInline):
    model = VideoQuestionAnswers
    extra = 1


class EssayQuestionAnswersInline(admin.TabularInline):
    model = EssayQuestionAnswers
    extra = 1


class UploadPhotoQuestionAnswersInline(admin.TabularInline):
    model = UploadPhotoQuestionAnswers
    extra = 1


class ShortQuestionAnswersInline(admin.TabularInline):
    model = ShortQuestionAnswers
    extra = 1


class NumericQuestionAnswersInline(admin.TabularInline):
    model = NumericQuestionAnswers
    extra = 1


class DropDownQuestionAnswersInline(admin.TabularInline):
    model = DropDownQuestionAnswers
    extra = 1


class PercentageQuestionAnswersInline(admin.TabularInline):
    model = PercentageQuestionAnswers
    extra = 1


class MCQQuestionAnswersInline(admin.TabularInline):
    model = MCQQuestionAnswers
    extra = 1


class ExitQuestionAnswersInline(admin.TabularInline):
    model = ExitQuestionAnswers
    extra = 1


@admin.register(OrderDetail)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        StudentTaskStatusInline,
        VideoQuestionAnswersInline,
        EssayQuestionAnswersInline,
        UploadPhotoQuestionAnswersInline,
        ShortQuestionAnswersInline,
        NumericQuestionAnswersInline,
        DropDownQuestionAnswersInline,
        PercentageQuestionAnswersInline,
        MCQQuestionAnswersInline,
        ExitQuestionAnswersInline,
    ]

    fieldsets = (
        (
            "Product",
            {
                "fields": (
                    "id",
                    "order",
                    "project",
                    "number_of_points",
                    "expire_on",
                    "is_expire",
                    "is_active",
                    "is_delete",
                    "is_complete",
                    "activity_status",
                    "report_file",
                    "qr_code_verification",
                    "student_activity_certificate_file",
                    "student_activity_certificate_page_1_to_5_file",
                    "student_activity_chapters",
                    "report_generate_date",
                )
            },
        ),
    )

    list_display = (
        "id",
        "order",
        "project",
        "number_of_points",
        "expire_on",
        "is_expire",
        "is_active",
    )
    readonly_fields = ("id",)
    # search_fields = ('product_name__item_name',)
