from django.urls import include, path
from rest_framework import routers

from activityngo.discount import api

router = routers.SimpleRouter()

router.register("discount-code", api.DiscountViewSet, basename="discount")
router.register("discount-usage", api.DiscountUsageViewSet, basename="discount-usage")
# router.register('discount-code', api.DiscountCodeViewSet, basename='discount-code')

app_name = "discount"

urlpatterns = [
    path("", include(router.urls)),
]
