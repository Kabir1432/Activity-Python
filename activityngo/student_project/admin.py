from django.contrib import admin

from activityngo.student_project.models import (DropDownQuestionAnswers,
                                                EssayQuestionAnswers,
                                                ExitQuestionAnswers,
                                                MCQQuestionAnswers,
                                                NumericQuestionAnswers,
                                                PercentageQuestionAnswers,
                                                ShortQuestionAnswers,
                                                StudentTaskStatus,
                                                SurveysDetails,
                                                UploadPhotoQuestionAnswers,
                                                VideoQuestionAnswers)

# Register your models here.
admin.site.register(StudentTaskStatus)
admin.site.register(VideoQuestionAnswers)
admin.site.register(EssayQuestionAnswers)
admin.site.register(UploadPhotoQuestionAnswers)
admin.site.register(ShortQuestionAnswers)
admin.site.register(NumericQuestionAnswers)
admin.site.register(DropDownQuestionAnswers)
# admin.site.register(DropDownSelectedOptions )
admin.site.register(PercentageQuestionAnswers)
admin.site.register(MCQQuestionAnswers)
admin.site.register(ExitQuestionAnswers)
# admin.site.register(ExitSelectedOptions)
admin.site.register(SurveysDetails)
