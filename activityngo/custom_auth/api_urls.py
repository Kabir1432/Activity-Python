from django.urls import include, path
from rest_framework import routers
from unicef_restlib.routers import NestedComplexRouter

from activityngo.custom_auth import api

router = routers.SimpleRouter()
router.register("v1/auth", api.UserAuthViewSet, basename="auth")
router.register("v1/users", api.UserViewSet, basename="users")
router.register("v1/walkthrough", api.WalkthroughViewSet, basename="walkthrough")
router.register(
    "v1/walkthrough-slides", api.WalkthroughSlidesViewSet, basename="walkthrough-slides"
)


# for walkthrough multiple photo
walkthrough_router = NestedComplexRouter(router, r"v1/walkthrough")
walkthrough_router.register(
    r"walkthrough-photos", api.WalkthroughMediaViewSet, basename="walkthrough-photos"
)

app_name = "custom-auth"

urlpatterns = [
    path("", include(router.urls)),
    path("", include(walkthrough_router.urls)),
]
