from django.urls import include, path
from rest_framework import routers

from activityngo.college import api

router = routers.SimpleRouter()

router.register("v1/college", api.CollegeViewSet, basename="college")
router.register(
    "v1/college-degree", api.CollegeDegreeViewSet, basename="college-degree"
)
router.register("v1/degree-branch", api.DegreeBranchViewSet, basename="degree-branch")
router.register(
    "v1/branch-batches", api.BranchBatchesViewSet, basename="branch-batches"
)

router.register(
    "v1/college-collaboration",
    api.CollegeCollaborationViewSet,
    basename="college-collaboration",
)

router.register("v1/college_users", api.CollegeUsersViewSet, basename="college_users")
router.register("v1/college-CMS", api.CollegeCMSViewSet, basename="college-CMS")

app_name = "college"

urlpatterns = [
    path("", include(router.urls)),
    path("<slug:slug>/", api.CMSDetail.as_view()),
    path("cms/<slug:slug>/", api.CollegeCMSDetail.as_view()),
]
