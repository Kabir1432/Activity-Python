from django.urls import include, path
from rest_framework import routers
from activityngo.order import api

router = routers.SimpleRouter()

router.register("order", api.OrderViewSet, basename="order")
router.register("order-details", api.OrderDetailsViewSet, basename="order")
router.register("get-complete-project-list", api.GetCompleteProjectListViewSet, basename="get_complete_project_list")
router.register("gst-details", api.GSTCategoryViewSet, basename="gst-details")

app_name = "order"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "razorpay-status/",
        api.RazorPayViewSet.as_view(),
        name="razorpay-status",
    ),
    path('razorpay-webhook/', api.razorpay_webhook_api, name='razorpay-webhook-api'),
    path("student-order/<int:id>/", api.student_order, name="student-order"),
    path('generate-report/', api.GenerateReportAPIView.as_view(), name='generate-report'),
    path('send-report/', api.SendReportAPIView.as_view(), name='send-report'),
]
