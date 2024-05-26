from django.urls import include, path
from rest_framework import routers

from activityngo.entities import api

router = routers.SimpleRouter()

router.register("v1/state", api.StateViewSet, basename="state")
router.register("v1/degree", api.DegreeViewSet, basename="degree")
router.register("v1/branch", api.BranchViewSet, basename="branch")
# router.register('v1/batches', api.BatchesViewSet, basename='batches')
router.register(
    "v1/project-category", api.ProjectCategoryViewSet, basename="project-category"
)
router.register("v1/project-type", api.ProjectTypeViewSet, basename="project-type")
router.register("v1/batch", api.BatchViewSet, basename="batch")
router.register("v1/implementation-batches", api.ImplementationBatchesViewSet, basename="implementation-batches")

app_name = "entities"

urlpatterns = [
    path("", include(router.urls)),
]
