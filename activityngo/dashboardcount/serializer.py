from rest_framework import serializers

from .models import AppDownload


class AppDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppDownload
        fields = ("download_count",)
