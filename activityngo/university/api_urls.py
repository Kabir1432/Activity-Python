from django.urls import include, path
from rest_framework import routers

from activityngo.university import api

router = routers.SimpleRouter()

router.register("v1/university", api.UniversityViewSet, basename="university")
router.register(
    "v1/university-collaboration",
    api.UniversityCollaborationViewSet,
    basename="university-collaboration",
)
router.register("v1/rules", api.UniversityRulesViewset, basename="university-rules")
router.register(
    "v1/university-CMS", api.UniversityCMSViewSet, basename="university-CMS"
)

app_name = "university"

urlpatterns = [
    path("", include(router.urls)),
    path("<slug:slug>/", api.CMSDetail.as_view()),
    path("cms/<slug:slug>/", api.UniversityCMSDetail.as_view()),
]
