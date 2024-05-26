from django.urls import include, path
from rest_framework import routers

from activityngo.cms import api

router = routers.SimpleRouter()
router.register("cms", api.CMSViewSet, basename="faq")
router.register("user-manual", api.UserManualViewSet, basename="user-manual")
router.register("faq", api.FAQViewSet, basename="faq")
router.register("contact-us-form", api.ContactUSFormViewSet, basename="contact-us-form")
router.register("contact-us", api.ContactUSViewSet, basename="contact-us")
router.register(
    "my-cart-instructions",
    api.MyCartInstructionsViewSet,
    basename="my-cart-instructions",
)

app_name = "cms"

urlpatterns = [
    path("", include(router.urls)),
    path("<slug:slug>/", api.CMSDetail.as_view()),
]
