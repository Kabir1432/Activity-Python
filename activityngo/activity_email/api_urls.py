from django.urls import include, path
from rest_framework import routers

from activityngo.activity_email import api

router = routers.SimpleRouter()

# router.register('activity-report', api.ReportContentSet, basename='activity_report')

app_name = "activity_email"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "send-email-student-download/",
        api.SendEmailToDownload.as_view(),
        name="send-email",
    ),
]
