from django.urls import include, path
from rest_framework import routers

from activityngo.student_project import api

router = routers.SimpleRouter()

router.register(
    "student_project", api.StudentProjectDetailsViewSet, basename="student-project"
)
router.register(
    "student-answers", api.StudentAnswersViewSet, basename="student-answers"
)
router.register("task-survey", api.SurveysDetailsViewSet, basename="task-survey")
router.register(
    "student-task-status", api.StudentTaskStatusViewSet, basename="student-task-status"
)
# router.register('survey-task-3', api.SurveyTask3ViewSet, basename='survey-task-3')
app_name = "student_project"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "survey-task-3/task-3-survey/",
        api.SurveyTask3ViewSet.as_view(),
        name="survey-task-3",
    ),
    path(
        "task-9-submit/",
        api.SubmitTask9ViewSet.as_view(),
        name="survey-task-3",
    ),
]
