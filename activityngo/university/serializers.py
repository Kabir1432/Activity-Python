from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from activityngo.entities.serializers import StateSerializer
from activityngo.university.models import (University, UniversityCMS,
                                           UniversityCollaboration,
                                           UniversityRules)


class UniversitySerializer(serializers.ModelSerializer):
    state_detail = StateSerializer(source="state", read_only=True, many=True)

    class Meta:
        model = University
        fields = [
            "id",
            "name",
            "address",
            "state",
            "project_category",
            "disable_date",
            "state_detail",
            "is_active",
        ]
        extra_kwargs = {
            "state": {"required": True},
            "project_category": {"required": True},
        }

    def update(self, instance, validated_data):
        """Delete can be done only after the 90 days of DISABLE"""

        instance = super().update(instance, validated_data)
        if instance.is_active is False:
            current_time = timezone.now()
            instance.disable_date = current_time
            instance.save()
        elif instance.is_active is True:
            instance.disable_date = None
            instance.save()
        return instance

    def get_fields(self):
        fields = super().get_fields()

        # Check if the context contains the update operation
        view = self.context.get("view")
        if view and hasattr(view, "action"):
            if (
                    self.context["view"].action == "update"
                    or self.context["view"].action == "partial_update"
            ):
                # Add field names to be read-only during update
                readonly_fields = ["disable_date"]
                for field_name in readonly_fields:
                    if field_name in fields:
                        fields[field_name].read_only = True
        return fields


class UniversityRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityRules
        fields = ["id", "university", "meta_value"]

    def validate(self, attrs):
        if UniversityRules.objects.filter(university=attrs["university"]).exists():
            raise serializers.ValidationError(_("University rules is already added."))
        return super().validate(attrs)


class UniversityCollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityCollaboration
        fields = ["id", "meta_key", "meta_value", "slug"]


class UniversityCMSSerializer(serializers.ModelSerializer):
    university_cms_page_url = serializers.SerializerMethodField()

    class Meta:
        model = UniversityCMS
        fields = (
            "id",
            "university",
            "meta_key",
            "slug",
            "meta_value",
            "university_cms_page_url",
        )
        read_only = ("id",)
        # extra_kwargs = {
        #     '_name': {'required': True},
        # }

    def get_university_cms_page_url(self, obj):
        request = self.context.get("request")
        if request:
            # Get the current domain and port from the request
            current_scheme = request.scheme
            current_domain = request.META["HTTP_HOST"]
            # Extract the path from the hardcoded URL
            url_path = f"/api/university/{obj.slug}"
            # Construct the dynamic URL using the current scheme, domain, and the extracted path
            return f"{current_scheme}://{current_domain}{url_path}"
        else:
            return ""
