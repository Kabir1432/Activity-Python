from django.urls import include, path
from rest_framework.routers import SimpleRouter

from activityngo.notification.api import PushNotificationViewSet

router = SimpleRouter()

router.register("v1", PushNotificationViewSet, basename="notification")


app_name = "notification"

urlpatterns = [
    path("", include(router.urls)),
]
