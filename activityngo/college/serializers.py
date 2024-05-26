from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from activityngo.college.models import (
    BranchBatches,
    College,
    CollegeCMS,
    CollegeCollaboration,
    CollegeDegree,
    CollegeUsers,
    DegreeBranch,
)
from activityngo.custom_auth.models import ApplicationUser
from activityngo.ngo.serializers import UniversitySerializer
from activityngo.university.models import University


class BranchBatchesSerializer(serializers.ModelSerializer):
    batches_year = serializers.SerializerMethodField()
    degree_name = serializers.CharField(
        source="degree_branch.college_degree.degree.name", read_only=True
    )
    branch_name = serializers.CharField(
        source="degree_branch.branch.name", read_only=True
    )

    class Meta:
        model = BranchBatches
        fields = [
            "id",
            "degree_branch",
            "branch_name",
            "degree_name",
            "batches",
            "batches_year",
            "is_active",
            "disable_date",
        ]

    extra_kwargs = {
        "degree_branch": {"required": True},
        "batches": {"required": True},
    }

    def get_batches_year(self, obj):
        try:
            return f"{obj.batches.start_year}-{obj.batches.end_year}"
        except:
            return ""

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


class DegreeBranchSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    college_degree_batches_data = BranchBatchesSerializer(
        source="college_degree_batches", many=True, read_only=True
    )
    degree_name = serializers.CharField(
        source="college_degree.degree.name", read_only=True
    )

    class Meta:
        model = DegreeBranch
        fields = [
            "id",
            "college_degree",
            "degree_name",
            "branch",
            "branch_name",
            "college_degree_batches_data",
            "is_active",
            "disable_date",
        ]
        extra_kwargs = {
            "college_degree": {"required": True},
            "degree": {"required": True},
        }

    def get_branch_name(self, obj):
        try:
            return obj.branch.name
        except:
            return ""

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


class CollegeDegreeSerializer(serializers.ModelSerializer):
    degree_name = serializers.SerializerMethodField()
    colleges_degree_data = DegreeBranchSerializer(
        source="college_degree_branch", many=True, read_only=True
    )

    class Meta:
        model = CollegeDegree
        fields = [
            "id",
            "college",
            "degree",
            "degree_name",
            "colleges_degree_data",
            "is_active",
            "disable_date",
        ]
        extra_kwargs = {
            "college": {"required": True},
            "degree": {"required": True},
        }

    def get_degree_name(self, obj):
        try:
            return obj.degree.name
        except:
            return ""

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


class CollegeListSerializer(serializers.ModelSerializer):
    university_data = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = [
            "id",
            "name",
            "address",
            "state",
            "university_data",
            "state_name",
            "university",
            "is_active",
            "disable_date",
            "is_active",
        ]

    def get_university_data(self, obj):
        try:
            university_data = [
                UniversitySerializer(university_data).data
                for university_data in obj.university.all()
            ]
            return university_data
        except:
            return ""

    def get_state_name(self, obj):
        try:
            return obj.state.name
        except:
            return ""


class CollegeSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()
    university = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.all(),
        many=True,
        read_only=False,
    )
    university_data = serializers.SerializerMethodField()
    colleges_degree_data = CollegeDegreeSerializer(
        source="colleges_degree", many=True, read_only=True
    )

    class Meta:
        model = College
        fields = [
            "id",
            "name",
            "address",
            "state",
            "university",
            "is_active",
            "disable_date",
            "branch_name",
            "state_name",
            "is_active",
            "university_data",
            "colleges_degree_data",
        ]
        extra_kwargs = {
            "state": {"required": True},
            "university": {"required": True},
            "branch": {"required": True},
        }

    def get_university_data(self, obj):
        try:
            university_data = [
                UniversitySerializer(university_data).data
                for university_data in obj.university.all()
            ]
            return university_data
        except:
            return ""

    def get_branch_name(self, obj):
        try:
            return obj.branch.name
        except:
            return ""

    def get_state_name(self, obj):
        try:
            return obj.state.name
        except:
            return ""

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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ApplicationUser
        fields = (
            "username",
            "email",
            "fullname",
            "phone",
            "gender",
            "user_type",
            "date_joined",
            "password",
        )
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "fullname": {"required": True},
            "phone": {"required": True},
            "gender": {"required": True},
            "date_joined": {"required": False},
            "password": {"required": False},
            "user_type": {"required": True},
        }

    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)

        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user


class CollegeUsersSerializer(serializers.ModelSerializer):
    college_detail = CollegeSerializer(source="college", read_only=True)
    user_detail = UserSerializer(source="user", read_only=True)
    user_data = serializers.JSONField(write_only=True)
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = CollegeUsers
        fields = [
            "id",
            "user",
            "access_url",
            "state",
            "university",
            "college",
            "degree",
            "branch",
            "branch_name",
            "report_link",
            "is_active",
            "disable_date",
            "user_data",
            "college_detail",
            "user_detail",
            "is_active",
        ]
        extra_kwargs = {
            "access_url": {"required": True},
            "state": {"required": True},
            "university": {"required": True},
            "college": {"required": True},
            "degree": {"required": True},
            "branch": {"required": True},
        }

    def get_branch_name(self, obj):
        try:
            return obj.branch.branch.name
        except:
            return ""

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user_data")
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        validated_data["user"] = user
        return super().create(validated_data)

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

        # update user data
        if "user_data" in validated_data:
            parent_data = validated_data.pop("user_data")
            parent_serializer = UserSerializer(
                instance.user, data=parent_data, partial=True
            )
            parent_serializer.is_valid(raise_exception=True)
            parent_serializer.save()

        return instance

    def get_fields(self):
        fields = super().get_fields()

        view = self.context.get("view")
        if view and hasattr(view, "action"):
            if (
                    self.context["view"].action == "update"
                    or self.context["view"].action == "partial_update"
            ):
                # Add field names to be read-only during update
                readonly_fields = ["disable_date", "access_url", "user", "report_link"]
                for field_name in readonly_fields:
                    if field_name in fields:
                        fields[field_name].read_only = True
        return fields


class CollegeCollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeCollaboration
        fields = ["id", "meta_key", "meta_value", "slug"]


class CollegeCMSSerializer(serializers.ModelSerializer):
    college_cms_page_url = serializers.SerializerMethodField()

    class Meta:
        model = CollegeCMS
        fields = (
            "id",
            "college",
            "meta_key",
            "slug",
            "meta_value",
            "college_cms_page_url",
        )
        read_only = ("id",)

    def get_college_cms_page_url(self, obj):
        request = self.context.get("request")
        if request:
            # Get the current domain and port from the request
            current_scheme = request.scheme
            current_domain = request.META["HTTP_HOST"]
            # Extract the path from the hardcoded URL
            url_path = f"/api/college/{obj.slug}"
            # Construct the dynamic URL using the current scheme, domain, and the extracted path
            return f"{current_scheme}://{current_domain}{url_path}"
        else:
            return ""
