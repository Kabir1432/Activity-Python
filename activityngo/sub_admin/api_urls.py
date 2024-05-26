from django.urls import include, path
from rest_framework import routers

from activityngo.sub_admin import api

router = routers.SimpleRouter()

router.register("v1/admin", api.SubAdminViewSet, basename="sub-admin")
router.register("permission", api.CustomPermissionViewSet, basename="permission")
router.register(
    "user-permission", api.UserAccessPermissionViewSet, basename="user-permission"
)
router.register(
    "sub-admin-access-log",
    api.SubAdminAccessLogViewSet,
    basename="sub-admin-access-log",
)
router.register("sub-admin-auth", api.SubAdminAuthViewSet, basename="sub-admin-auth")

app_name = "sub_admin"

urlpatterns = [
    path("", include(router.urls)),
    path("send-reset-email/", api.send_reset_email, name="send_reset_email"),
    path("reset-password/", api.reset_password, name="reset-password"),
    path(
        "bulk-update-user-access-permission/",
        api.UserAccessPermissionBulkUpdate.as_view(),
        name="bulk-update-user-access-permission",
    ),
]
