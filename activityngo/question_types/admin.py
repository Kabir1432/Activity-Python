from django.contrib import admin

from activityngo.question_types.models import (EssayQuestion, ExitTestQuestion,
                                               ExitTestQuestionOption,
                                               McqOption, MCQQuestion,
                                               NumericQuestion,
                                               PercentageQuestion,
                                               ShortAnswerQuestion,
                                               UploadPhotoQuestion,
                                               VideoQuestion)

# Register your models here.
admin.site.register(VideoQuestion)
admin.site.register(EssayQuestion)
admin.site.register(ShortAnswerQuestion)
admin.site.register(NumericQuestion)
admin.site.register(PercentageQuestion)
admin.site.register(MCQQuestion)
admin.site.register(McqOption)
admin.site.register(UploadPhotoQuestion)
admin.site.register(ExitTestQuestion)
admin.site.register(ExitTestQuestionOption)
