from django.urls import include, path
from rest_framework import routers

from activityngo.project import api

router = routers.SimpleRouter()

router.register("project", api.ProjectViewSet, basename="project")
router.register(
    "project-details", api.ProjectDetailsViewSet, basename="project-details"
)
router.register("student-feedback", api.StudentFeedbackViewSet, basename="student-feedback")
router.register("special-power", api.SpecialPowerViewSet, basename="special-power")

app_name = "project"

urlpatterns = [
    path("", include(router.urls)),
]
