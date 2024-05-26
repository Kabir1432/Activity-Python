from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import gettext as _
from activityngo.entities.models import (Batches, Branch, Degree,
                                         ProjectCategory, ProjectType, State, ImplementationBatches)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name", "is_active", "disable_date"]

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
                    self.context.get("view").action == "update"
                    or self.context.get("view").action == "partial_update"
            ):
                # Add field names to be read-only during update
                readonly_fields = ["disable_date"]
                for field_name in readonly_fields:
                    if field_name in fields:
                        fields[field_name].read_only = True
        return fields


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ["id", "name", "is_active", "disable_date"]

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


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "is_active", "disable_date"]

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


# class BatchesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Batches
#         fields = ['id', 'name']


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ["id", "name", "is_active", "disable_date"]

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


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ["id", "type", "is_active", "disable_date"]

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


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batches
        fields = ["id", "start_year", "end_year", "is_active", "disable_date"]

        extra_kwargs = {
            "start_year": {"required": True},
            "end_year": {"required": True},
            "disable_date": {"read_only": True},
        }

    def validate(self, data):
        if data.get('start_year') and data.get('end_year'):
            if data['start_year'] >= data['end_year']:
                raise serializers.ValidationError({'end_year': _('End Year must be greater than Start Year')})
        return data

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


class ImplementationBatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImplementationBatches
        fields = ["id", "start_year", "end_year", "is_active", "disable_date"]

        extra_kwargs = {
            "start_year": {"required": True},
            "end_year": {"required": True},
            "disable_date": {"read_only": True},
        }

    def validate(self, data):
        if data.get('start_year') and data.get('end_year'):
            if data['start_year'] >= data['end_year']:
                raise serializers.ValidationError({'end_year': _('End Year must be greater than Start Year')})
        return data

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