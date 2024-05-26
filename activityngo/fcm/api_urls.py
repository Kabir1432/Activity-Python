from django.urls import include, path
from rest_framework import routers

from activityngo.fcm.api import CustomFCMDeviceViewSet, PushNotificationViewSet

router = routers.SimpleRouter()

router.register("devices", CustomFCMDeviceViewSet)
router.register("notifications", PushNotificationViewSet, basename="notifications")
app_name = "fcm"

urlpatterns = [
    path("", include(router.urls)),
]
