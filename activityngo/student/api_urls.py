from django.urls import include, path
from rest_framework.routers import SimpleRouter
from unicef_restlib.routers import NestedComplexRouter
from activityngo.student import api

router = SimpleRouter()

router.register("v1", api.StudentViewSet, basename="student-auth")

router.register("v1/about-us", api.AboutUsViewSet, basename="about-us")
router.register(
    "v1/term-condition", api.TermsConditionViewSet, basename="term-condition"
)
router.register("v1/our-team", api.OurTeamViewSet, basename="our-team")
router.register("v1/necessity", api.NecessityViewSet, basename="necessity")
router.register("v1/aicte-rules", api.AicteRulesViewSet, basename="aicte-rules")
router.register(
    "v1/implementation-method",
    api.ImplementationMethodViewSet,
    basename="implementation-method",
)
router.register("v1/complaint", api.ComplaintViewSet, basename="complaint")

router.register("student", api.StudentDetailsViewSet, basename="student")

# for complaint multiple photo
complaint_router = NestedComplexRouter(router, r"v1/complaint")
complaint_router.register(
    r"complaint-photos", api.ComplaintMediaViewSet, basename="walkthrough-photos"
)

app_name = "student"

urlpatterns = [
    path("", include(router.urls)),
    path("", include(complaint_router.urls)),
    path('grammar-check/', api.GrammarCheckView.as_view(), name='grammar-check'),

]
