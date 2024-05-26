from django.urls import include, path
from rest_framework import routers

from activityngo.dashboardcount import api

router = routers.SimpleRouter()

# router.register('cart', api.CartViewSet, basename='cart')

app_name = "dashboardcount"

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard-count/", api.DashboardCountView.as_view()),
    path(
        "increment-download-count/",
        api.IncrementDownloadCount.as_view(),
    ),
]
