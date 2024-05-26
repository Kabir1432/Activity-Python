from django.utils.translation import gettext as _
from rest_framework import serializers

from activityngo.activity_report.models import ReportContent


class ReportContentSerializer(serializers.ModelSerializer):
    project_title = serializers.SerializerMethodField()
    ngo_name = serializers.SerializerMethodField()

    class Meta:
        model = ReportContent
        fields = [
            "id",
            "project",
            "project_title",
            "ngo_name",
            "type_point",
            "disclaimer",
            "abstract",
            "chapter_01",
            "chapter_02",
            "chapter_03",
            "chapter_04",
            "chapter_05",
            "chapter_06",
            "chapter_07",
            "appendix",
            "is_active",
        ]
        extra_kwargs = {
            "project": {"required": True},
            "type_point": {"required": True},
            # 'disclaimer': {'required': True},
        }

    def get_project_title(self, obj):
        try:
            return obj.project.title
        except:
            return ""

    def get_ngo_name(self, obj):
        try:
            return obj.project.franchise_ngo_name.ngo_name
        except:
            return ""
