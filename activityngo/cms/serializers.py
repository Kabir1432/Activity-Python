from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activityngo.cms.models import (
    CMS,
    FAQ,
    ContactUS,
    ContactUSForm,
    UserManual,
    MyCartInstructions,
)


class CMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMS
        fields = ("id", "meta_key", "slug", "meta_value")


class UserManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManual
        fields = (
            "id",
            "buy_projects_text_tutorial",
            "buy_projects_screenshot_tutorial",
            "buy_projects_video_url",
            "complete_tasks_text_tutorial",
            "complete_tasks_screenshot_tutorial",
            "complete_tasks_video_url",
            "resubmit_wrong_answers_text_tutorial",
            "resubmit_wrong_answers_screenshot_tutorial",
            "resubmit_wrong_answers_video_url",
            "how_to_complete_task_1",
            "project_task_file_1",
            "how_to_complete_task_2",
            "project_task_file_2",
            "how_to_complete_task_3",
            "project_task_file_3",
            "how_to_complete_task_4",
            "project_task_file_4",
            "how_to_complete_task_5",
            "project_task_file_5",
            "how_to_complete_task_6",
            "project_task_file_6",
            "how_to_complete_task_7",
            "project_task_file_7",
            "how_to_complete_task_8",
            "project_task_file_8",
            "how_to_complete_task_9",
            "project_task_file_9",
            "how_to_complete_task_10",
            "project_task_file_10",
            "how_to_complete_task_11",
            "project_task_file_11",
            "other_text_tutorial",
            "other_screenshot_tutorial",
            "other_projects_video_url",
            "task_1",
            "task_2",
            "task_3",
            "task_4",
            "task_5",
            "task_6",
            "task_7",
            "task_8",
            "task_9",
            "task_10",
            "task_11",
            "how_to_complete_tasks_20_points",
            "how_to_complete_tasks_10_points",
            "how_to_complete_tasks_05_points",
        )
        extra_kwargs = {
            "buy_projects_text_tutorial": {"required": True},
            "buy_projects_screenshot_tutorial": {"required": True},
            "buy_projects_video_url": {"required": True},
            "complete_tasks_text_tutorial": {"required": True},
            "complete_tasks_screenshot_tutorial": {"required": True},
            "complete_tasks_video_url": {"required": True},
            "resubmit_wrong_answers_text_tutorial": {"required": True},
            "resubmit_wrong_answers_screenshot_tutorial": {"required": True},
            "project_task_file_1": {"required": True},
            "project_task_file_2": {"required": True},
            "project_task_file_3": {"required": True},
            "project_task_file_4": {"required": True},
            "project_task_file_5": {"required": True},
            "project_task_file_6": {"required": True},
            "project_task_file_7": {"required": True},
            "project_task_file_8": {"required": True},
            "project_task_file_9": {"required": True},
            "project_task_file_10": {"required": True},
            "project_task_file_11": {"required": True},
            "other_text_tutorial": {"required": True},
            "other_screenshot_tutorial": {"required": True},
            "other_projects_video_url": {"required": True},
        }

    def create(self, request, *args, **kwargs):
        # Check if a GSTCategory instance already exists
        existing_instance = UserManual.objects.first()
        if existing_instance:
            raise ValidationError(_("Only one User Manual instance is allowed."))

        return super().create(request, *args, **kwargs)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answers"]


class ContactUSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUS
        fields = [
            "id",
            "phone",
            "visit_at",
            "filled_form_to_be_emailed_to",
            "whatsapp_phone",
        ]
        extra_kwargs = {
            "phone": {"required": True},
            "visit_at": {"required": True},
            "filled_form_to_be_emailed_to": {"required": True},
            "whatsapp_phone": {"required": True},
        }

    def create(self, request, *args, **kwargs):
        # Check if a GSTCategory instance already exists
        existing_instance = ContactUS.objects.first()
        if existing_instance:
            raise ValidationError(_("Only one Contact US instance is allowed."))

        return super().create(request, *args, **kwargs)


class MyCartInstructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCartInstructions
        fields = [
            "id",
            "instructions",
        ]
        extra_kwargs = {
            "instructions": {"required": True},
        }

    def create(self, request, *args, **kwargs):
        # Check if a GSTCategory instance already exists
        existing_instance = MyCartInstructions.objects.first()
        if existing_instance:
            raise ValidationError(
                _("Only one My Cart Instructions instance is allowed.")
            )

        return super().create(request, *args, **kwargs)


class ContactUSFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUSForm
        fields = [
            "id",
            "user",
            "firstname",
            "lastname",
            "email",
            "subject",
            "description",
        ]
        extra_kwargs = {
            "firstname": {"required": True},
            "lastname": {"required": True},
            "email": {"required": True},
            "subject": {"required": True},
            "description": {"required": True},
        }

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get("user") or self.context.get("request").user
        validated_data["user"] = user
        return super().create(validated_data)
