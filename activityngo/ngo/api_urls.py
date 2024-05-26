from django.urls import include, path
from rest_framework import routers

from activityngo.ngo import api

router = routers.SimpleRouter()

router.register("v1/ngo", api.NgoViewSet, basename="ngo")
router.register(
    "v1/ngo-collaboration", api.NGOCollaborationViewSet, basename="ngo-collaboration"
)
router.register("v1/ngo-franchise", api.FranchiseViewSet, basename="franchise")
router.register("v1/organization", api.OrganizationViewSet, basename="organization")
router.register("v1/directors", api.DirectorsViewSet, basename="directors")
router.register("v1/bank", api.BankViewSet, basename="bank")
router.register(
    "v1/organization-attachments",
    api.OrganizationAttachmentsViewSet,
    basename="organization-attachments",
)
router.register("v1/Ngo-CMS", api.NgoCMSViewSet, basename="Ngo-CMS")

app_name = "ngo"

urlpatterns = [
    path("", include(router.urls)),
    path("<slug:slug>/", api.CMSDetail.as_view()),
    path("cms/<slug:slug>/", api.NgoCMSDetail.as_view()),
]
