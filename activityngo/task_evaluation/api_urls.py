from django.urls import include, path
from rest_framework import routers
from activityngo.task_evaluation import api

router = routers.SimpleRouter()

router.register(
    "task-evaluation-05",
    api.EvaluationFor05PointProjectViewSet,
    basename="task-05-evaluation",
)
router.register(
    "task-evaluation-10",
    api.EvaluationFor10PointProjectViewSet,
    basename="task-10-evaluation",
)
router.register(
    "task-evaluation-20",
    api.EvaluationFor20PointProjectViewSet,
    basename="task-20-evaluation",
)
router.register(
    "dynamic-evaluation", api.DynamicEvaluationViewSet, basename="dynamic-evaluation"
)
router.register("task-3-status", api.Task3StatusViewSet, basename="Task-3-Status")


app_name = "task_evaluation"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "student-evaluation-status/<int:order_details>/",
        api.StudentEvaluationStatusViewSet.as_view(),
    ),
    path(
        "get-task-3-evaluation/",
        api.GetTaks03ViewSet.as_view(),
        name="get-task-3-evaluation",
    ),
]
