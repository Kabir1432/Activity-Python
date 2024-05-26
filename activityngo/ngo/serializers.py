from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activityngo.custom_auth.models import ApplicationUser
from activityngo.entities.models import State
from activityngo.ngo.models import (Bank, Directors, Franchise, Ngo, NgoCMS,
                                    NGOCollaboration, Organization,
                                    OrganizationAttachments)
from activityngo.university.models import University


# class UserDataNestedFieldMixin(object):
#     def create(self, validated_data):
#         post_styles = validated_data.pop('user_data', None)
#         # post_styles = {each.get('title'): each for each in post_styles}.values()
#
#         data = super().create(validated_data)
#
#         # for style in post_styles:
#         #     PostStyle.objects.create(post=post, title=style.get('title'), size=style.get('size'), url=style.get('url'),
#         #                              brand=style.get('brand'), price=style.get('price'))
#         return data


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
            "address",
            "user_type",
            "password",
        )
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "fullname": {"required": True},
            "phone": {"required": True},
            "gender": {"required": True},
            "address": {"required": True},
            "user_type": {"required": True},
            "password": {"required": True},
        }

    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)

        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user


class OrganizationAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationAttachments
        fields = [
            "id",
            "organization",
            "tagline",
            "llp_Certificate",
            "gstin_document",
            "udhyam_aadhar_document",
            "dpiit_document",
            "pan_card",
            "tan_card",
            "logo",
            "trustee_1_Aadhar_card",
            "trustee_2_aadhar_card",
            "cancelled_cheque",
            "seal_and_sign_of_director_1",
            "seal_and_sign_of_director_2",
            "ngo_office_photo",
            "seal_and_sign_of_trustee_3",
            "franchise_certificate",
            "trust_deed",
        ]
        extra_kwargs = {
            "organization": {"required": True},
            "tagline": {"required": False},
            "llp_Certificate": {"required": False},
            "gstin_document": {"required": False},
            "udhyam_aadhar_document": {"required": False},
            "dpiit_document": {"required": False},
            "pan_card": {"required": False},
            "tan_card": {"required": False},
            "logo": {"required": False},
            "trustee_1_Aadhar_card": {"required": False},
            "trustee_2_aadhar_card": {"required": False},
            "cancelled_cheque": {"required": False},
            "seal_and_sign_of_director_1": {"required": False},
            "seal_and_sign_of_director_2": {"required": False},
            "seal_and_sign_of_trustee_3": {"required": False},
            "franchise_certificate": {"required": False},
            "ngo_office_photo": {"required": False},
            "trust_deed": {"required": False},
        }


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = [
            "id",
            "organization",
            "account_name",
            "account_number",
            "account_type",
            "ifsc_code",
            "bank_name",
            "bank_branch",
            "upi_number",
            "mobile",
            "email",
        ]
        extra_kwargs = {
            "organization": {"required": True},
            "account_name": {"required": True},
            "account_number": {"required": True},
            "account_type": {"required": True},
            "ifsc_code": {"required": True},
            "bank_name": {"required": True},
            "bank_branch": {"required": True},
            "upi_number": {"required": True},
            "mobile": {"required": True},
            "email": {"required": True},
        }


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = [
            "id",
            "organization",
            "trustee_name",
            "designation",
            "director_no",
            "pan_no",
        ]
        extra_kwargs = {
            "organization": {"required": True},
            "trustee_name": {"required": True},
            "designation": {"required": True},
        }


class NgoCMSSerializer(serializers.ModelSerializer):
    organization_cms_page_url = serializers.SerializerMethodField()
    meta_key_value = serializers.SerializerMethodField()

    class Meta:
        model = NgoCMS
        fields = (
            "id",
            "organization",
            "meta_key",
            "meta_key_value",
            "slug",
            "meta_value",
            "organization_cms_page_url",
        )
        read_only = ("id",)
        extra_kwargs = {
            "ngo_name": {"required": True},
            "meta_key": {"required": True},
        }

    def get_meta_key_value(self, obj):
        value = (
            "About Us"
            if obj.meta_key == "about_us"
            else "Our Work"
            if obj.meta_key == "our_work"
            else "Activity Point Projects"
            if obj.meta_key == "activity_point_projects"
            else "Contact Us"
            if obj.meta_key == "contact_us"
            else ""
        )
        return value

    def get_organization_cms_page_url(self, obj):
        request = self.context.get("request")
        if request:
            # Get the current domain and port from the request
            current_scheme = request.scheme
            current_domain = request.META["HTTP_HOST"]
            # Extract the path from the hardcoded URL
            url_path = f"/api/ngo/{obj.slug}"
            # Construct the dynamic URL using the current scheme, domain, and the extracted path
            return f"{current_scheme}://{current_domain}{url_path}"
        else:
            return ""


class OrganizationSerializer(serializers.ModelSerializer):  # UserDataNestedFieldMixin
    # user_data_organization = UserSerializer(required=True, write_only=True, many=False)
    organization_bank = BankSerializer(read_only=True, many=False)
    organization_directors = DirectorSerializer(read_only=True, many=True)
    organization_cms = NgoCMSSerializer(read_only=True, many=True)
    organization_attachments = OrganizationAttachmentsSerializer(
        read_only=True, many=False
    )

    class Meta:
        model = Organization
        fields = [
            "id",
            "user",
            "organization_name",
            "franchise",
            "type",
            "address",
            "geo_tag",
            "organization_location_state",
            "email",
            "contact_no",
            "latitude",
            "longitude",
            "pan_no",
            "tan_no",
            "gstin",
            "udhyam_aadhar_certificate_number",
            "dpiit_certificate_number",
            "llpin",
            "website",
            "no_of_directors",
            "project_name",
            "organization_directors",
            "organization_bank",
            "organization_cms",
            "ngo_darpan_no",
            "cinno",
            "username",
            # 'user_data'
            "organization_attachments",
        ]
        extra_kwargs = {
            "type": {"required": True},
            "organization_name": {"required": True},
            "address": {"required": True},
            "organization_location_state": {"required": True},
            "geo_tag": {"required": True},
            "email": {"required": True},
            "contact_no": {"required": True},
            "latitude": {"required": True},
            "longitude": {"required": True},
            "pan_no": {"required": True},
            # "tan_no": {"required": True},
            "gstin": {"required": True},
            "udhyam_aadhar_certificate_number": {"required": True},
            "dpiit_certificate_number": {"required": True},
            "llpin": {"required": True},
            # "website": {"required": True},
            "no_of_directors": {"required": True},
            "project_name": {"required": True},
            # "ngo_darpan_no": {"required": True},
            # "cinno": {"required": True},
        }

    # @transaction.atomic
    # def create(self, validated_data):
    #     user_data = validated_data.pop('user_data_organization')
    #     user_serializer = UserSerializer(data=user_data)
    #     user_serializer.is_valid(raise_exception=True)
    #     user = user_serializer.save()
    #     validated_data['user'] = user
    #
    #     data = super().create(validated_data)
    #     return data


class FranchiseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )
    phone = PhoneNumberField(required=True, write_only=True)
    user_type = serializers.CharField(required=True, write_only=True)
    format_phone = serializers.SerializerMethodField()
    format_email = serializers.SerializerMethodField()
    franchise_organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Franchise
        fields = (
            "id",
            "user",
            "ngo",
            "entity_name",
            "entity_name_in_report",
            "address",
            "geo_tag",
            "gstin",
            "pan_no",
            "tan_no",
            "ngo_commission_percentage",
            "email",
            "phone",
            "user_type",
            "format_phone",
            "format_email",
            "franchise_organization",
        )
        read_only = ("id",)
        extra_kwargs = {
            "ngo": {"required": True},
            "entity_name": {"required": True},
            "entity_name_in_report": {"required": True},
            "address": {"required": True},
            "gstin": {"required": True},
            "pan_no": {"required": True},
            # "tan_no": {"required": True},
            "ngo_commission_percentage": {"required": True},
        }

    @transaction.atomic
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        instance = getattr(self, "instance", None)
        if instance is None:  # validation while creating obj
            if (
                    ApplicationUser.objects.filter(email=validated_data["email"]).exists()
                    or ApplicationUser.objects.filter(
                phone=validated_data["phone"]
            ).exists()
            ):
                raise ValidationError(
                    _("User already exists with this email or phone.")
                )
        else:  # validation while updating obj instance.user.email
            user = instance.user
            if user.email != validated_data["email"]:
                if ApplicationUser.objects.filter(
                        email=validated_data["email"]
                ).exists():
                    raise ValidationError(_("User already exists with this email."))
                else:
                    user.email = validated_data["email"]
            if user.phone != validated_data["phone"]:
                if ApplicationUser.objects.filter(
                        phone=validated_data["phone"]
                ).exists():
                    raise ValidationError(_("User already exists with this phone."))
                else:
                    user.phone = validated_data["phone"]
            user.save()
        return validated_data

    def get_format_phone(self, obj):
        try:
            return str(obj.user.phone)
        except:
            return ""

    def get_format_email(self, obj):
        try:
            return str(obj.user.email)
        except:
            return ""

    @transaction.atomic
    def create(self, validated_data):
        # new_dict = {key: validated_data[key] for key in ["email", "phone", ]}
        user, created = ApplicationUser.objects.get_or_create(
            email=validated_data["email"],
            phone=validated_data["phone"],
            user_type=validated_data["user_type"],
        )
        if not created:
            raise ValidationError(_("User already exists."))
        validated_data.pop("email", None)
        validated_data.pop("phone", None)
        validated_data.pop("user_type", None)
        validated_data["user"] = user
        data = super().create(validated_data)
        return data


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("id", "name")


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ("id", "name", "address")


class NgoSerializer(serializers.ModelSerializer):
    ngo_franchise = FranchiseSerializer(read_only=True)
    state = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(),
        many=True,
        read_only=False,
        # source='states'
    )
    university = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.all(),
        many=True,
        read_only=False,
        # source='states'
    )
    state_data = serializers.SerializerMethodField()
    university_data = serializers.SerializerMethodField()

    class Meta:
        model = Ngo
        fields = (
            "id",
            "ngo_name",
            "franchise_code",
            "state",
            "state_data",
            "university",
            "university_data",
            "ngo_franchise",
            "is_active",
            "is_delete",
            "disable_date",
        )
        read_only = ("id",)
        extra_kwargs = {
            "ngo_name": {"required": True},
            "state": {"required": True},
            "university": {"required": True},
        }

    def get_state_data(self, obj):
        try:
            state_data = [StateSerializer(state).data for state in obj.state.all()]
            return state_data
        except:
            return ""

    def get_university_data(self, obj):
        try:
            university_data = [
                UniversitySerializer(university_data).data
                for university_data in obj.university.all()
            ]
            return university_data
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


class NGOCollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGOCollaboration
        fields = ["id", "meta_key", "meta_value", "slug"]
