from django.urls import include, path
from rest_framework import routers

from activityngo.cart import api

router = routers.SimpleRouter()

router.register("cart", api.CartViewSet, basename="cart")

app_name = "cart"

urlpatterns = [
    path("", include(router.urls)),
]
