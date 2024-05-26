from rest_framework import serializers
from activityngo.website_content.models import WebsiteContent, WebsiteCoverPhoto


class WebsiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteContent
        fields = ("id", "domain", "page_name", "meta_value")


class WebsiteCoverPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteCoverPhoto
        fields = ("id", "domain", "cover_photo",)
