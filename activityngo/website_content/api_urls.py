from django.urls import include, path
from rest_framework import routers

from activityngo.website_content import api

router = routers.SimpleRouter()

router.register("website-content", api.WebsiteContentViewSet, basename="website_content")
router.register("website-cover-photos", api.WebsiteCoverPhotoViewSet, basename="website_cover_photos")

app_name = "website_content"

urlpatterns = [
    path("", include(router.urls)),
]
