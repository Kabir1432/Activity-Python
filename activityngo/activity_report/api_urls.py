from django.urls import include, path
from rest_framework import routers

from activityngo.activity_report import api

router = routers.SimpleRouter()

router.register("activity-report", api.ReportContentSet, basename="activity_report")

app_name = "activity_report"

urlpatterns = [
    path("", include(router.urls)),
    path("get-statistics/", api.GetStatisticsViewSet.as_view(), name="get-statistics"),
]
