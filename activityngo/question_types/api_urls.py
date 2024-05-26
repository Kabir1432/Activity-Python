from django.urls import include, path
from rest_framework import routers

from activityngo.question_types import api

router = routers.SimpleRouter()

router.register("video-question", api.VideoQuestionViewSet, basename="video-question")
router.register("essay-question", api.EssayQuestionViewSet, basename="essay-question")
router.register(
    "short-question", api.ShortAnswerQuestionViewSet, basename="short-question"
)
router.register(
    "number-question", api.NumericQuestionViewSet, basename="number-question"
)
router.register(
    "percentage-question", api.PercentageQuestionViewSet, basename="percentage-question"
)
router.register("mcq-question", api.MCQQuestionViewSet, basename="mcq-question")
router.register("mcq-option", api.MCQOptionViewSet, basename="mcq-option")
router.register(
    "upload-photo-question",
    api.UploadPhotoQuestionViewSet,
    basename="upload-photo-question",
)
router.register(
    "exit-test-question", api.ExitTestQuestionViewSet, basename="exit-test-question"
)
router.register(
    "exit-test-question-option",
    api.ExitTestQuestionOptionViewSet,
    basename="exit-test-question-option",
)
router.register(
    "drop-down-question", api.DropdownQuestionViewSet, basename="drop-down-question"
)
router.register(
    "drop-down-question-option",
    api.DropdownQuestionOptionViewSet,
    basename="drop-down-question-option",
)
router.register(
    "task-instruction", api.TaskInstructionsViewSet, basename="task-instruction"
)

app_name = "question_types"

urlpatterns = [
    path("", include(router.urls)),
]
