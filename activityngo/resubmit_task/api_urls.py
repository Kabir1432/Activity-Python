from django.urls import include, path
from rest_framework import routers

from activityngo.resubmit_task import api

router = routers.SimpleRouter()

router.register("", api.ResubmitTaskViewSet, basename="resubmit-task")

app_name = "resubmit_task"

urlpatterns = [
    path("", include(router.urls)),
]
