from django.urls import include, path
from rest_framework.routers import SimpleRouter

from activityngo.registrations.api import RegistrationViewSet

router = SimpleRouter()

router.register("v1", RegistrationViewSet, basename="registration")


app_name = "registration"

urlpatterns = [
    path("", include(router.urls)),
]
