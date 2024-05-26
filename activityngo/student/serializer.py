from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import (AuthenticationFailed, PermissionDenied,
                                       ValidationError)

from activityngo.cart.models import Cart
from activityngo.custom_auth.models import ApplicationUser
from activityngo.custom_auth.serializers import UserPhotoSerializer
from activityngo.fcm.models import PushNotification
from activityngo.notification.models import Notification
from activityngo.student.models import (AboutUs, AicteRules, Complaints,
                                        ComplaintsMedia, Implementation,
                                        Necessity, OurTeam, StudentDetails,
                                        TermsAndCondition)


class StudentDetailsEmptySerializer(serializers.Serializer):
    """
    defined empty serializer to use this serializer for Authentication.
    """

    pass


class StudentSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    fullname = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    phone = PhoneNumberField(required=True)
    address = serializers.CharField(required=True)
    device_type = serializers.CharField(required=True)
    device_token = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)
    os_version = serializers.CharField(required=False)
    device_name = serializers.CharField(required=False)
    model_name = serializers.CharField(required=False)
    ip_address = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    login_type = serializers.CharField(required=True)
    social_key = serializers.CharField(required=False)

    class Meta:
        model = StudentDetails
        fields = [
            "google_full_name",
            "email",
            "fullname",
            "gender",
            "phone",
            "address",
            "student_state",
            "college_state",
            "device_id",
            "university",
            "college",
            "degree",
            "branch",
            "batch",
            "id_number",
            "device_type",
            "device_token",
            "os_version",
            "device_name",
            "model_name",
            "ip_address",
            "password",
            "login_type",
            "social_key",
            "student_membership_id",
            "student_ip_address",
        ]
        extra_kwargs = {
            "student_ip_address": {"required": True},
        }

    def validate(self, attrs):
        if attrs["login_type"] not in ["S", "G"]:
            raise serializers.ValidationError(_("Login type choice is invalid."))
        elif attrs["login_type"] == "S" and not attrs.get("password", None):
            raise serializers.ValidationError(_("Password field is required."))
        elif attrs["login_type"] == "G" and not attrs.get("social_key", None):
            raise serializers.ValidationError(_("Social key field is required."))
        elif ApplicationUser.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(_("Email address already exists."))
        elif ApplicationUser.objects.filter(phone=attrs["phone"]).exists():
            raise serializers.ValidationError(_("Phone number already exists."))
        return super().validate(attrs)

    def create(self, validated_data):
        # add Application User details
        user_object = ApplicationUser.objects.create(
            email=validated_data.pop("email"),
            fullname=validated_data.pop("fullname"),
            gender=validated_data.pop("gender"),
            phone=validated_data.pop("phone"),
            address=validated_data.pop("address"),
            device_type=validated_data.pop("device_type"),
            device_token=validated_data.pop("device_token"),
            os_version=validated_data.pop("os_version", ""),
            device_name=validated_data.pop("device_name", ""),
            model_name=validated_data.pop("model_name", ""),
            ip_address=validated_data.pop("ip_address", ""),
            login_type=validated_data.pop("login_type"),
            social_key=validated_data.pop("social_key", ""),
            user_type="student",
            device_id=validated_data.pop("device_id"),
        )

        # Set ApplicationUser password if login type is 'S'
        # if validated_data.pop("login_type") == "S":

        if validated_data.get("password"):
            password = validated_data.pop("password")
            user_object.set_password(password)
            user_object.save(update_fields=["password"])

        validated_data["student"] = user_object
        return super().create(validated_data)


class StudentLoginSerializer(serializers.ModelSerializer):
    LOGIN_TYPES = (
        ("S", _("Simple")),
        ("G", _("Google")),
    )

    DEVICE_TYPES = (("A", _("Android")), ("I", _("IOS")))

    login_type = serializers.ChoiceField(
        LOGIN_TYPES,
        required=True,
        error_messages={
            "required": _("Login type field is required."),
            "blank": _("Login type field may not be blank."),
            "invalid_choice": _("Login type is not a valid choice."),
        },
    )
    social_key = serializers.CharField(
        max_length=512, allow_null=True, allow_blank=True, required=False
    )
    password = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )

    email = serializers.EmailField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )

    device_type = serializers.ChoiceField(
        DEVICE_TYPES,
        default="A",
        error_messages={
            "required": _("Device type field is required."),
            "blank": _("Device type field may not be blank."),
            "invalid_choice": _("Device type is not a valid choice."),
        },
    )
    device_token = serializers.CharField(
        required=True,
        error_messages={
            "required": _("Device token field is required."),
            "blank": _("Device token field may not be blank."),
        },
    )
    device_id = serializers.CharField(
        required=True,
        error_messages={
            "required": _("Device id field is required."),
            "blank": _("Device id field may not be blank."),
        },
    )
    os_version = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    device_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    model_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    ip_address = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    uuid_number = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    imei_number = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    app_version = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    api_version = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = ApplicationUser
        fields = [
            "login_type",
            "social_key",
            "email",
            "password",
            "device_type",
            "device_id",
            "device_token",
            "os_version",
            "device_name",
            "model_name",
            "ip_address",
            "uuid_number",
            "imei_number",
            "app_version",
            "api_version",
        ]

    def validate(self, attrs):
        login_type = attrs.get("login_type", None)

        if login_type == "S":
            email = attrs.get("email", None)
            password = attrs.get("password", None)
            if not email:
                raise AuthenticationFailed(_("Email field may not be blank."))
            if not password:
                raise AuthenticationFailed(_("Password field may not be blank."))
            try:
                user = ApplicationUser.objects.filter(
                    Q(phone=email) | Q(email=email),
                    is_delete=0,
                    is_superuser=0,
                    is_staff=0,
                    login_type=login_type,
                )
                if user[0].check_password(password):
                    user = user[0]
                else:
                    user = None
            except:
                user = None
        else:
            social_key = attrs.get("social_key", None)
            email = attrs.get("email", None)
            if not social_key:
                raise AuthenticationFailed(_("Social key field may not be blank."))

            user = ApplicationUser.objects.filter(
                email=email,
                social_key=social_key,
                login_type=login_type,
                is_delete=0,
                is_superuser=0,
                is_staff=0,
            )
            try:
                user = user[0]
            except:
                """
                * When user is not social login
                * Note : If u changed AuthenticationFailed Message than also changed renderer file
                """
                raise ValidationError(_("This email is not registered with us"))
                # raise AuthenticationFailed(_('This account is not register.'))

        if user is None:
            # raise AuthenticationFailed(_('Invalid Username or Password, Please Try Again.'))
            raise ValidationError(_("Invalid Username or Password, Please Try Again."))

        if not user.is_active:
            raise PermissionDenied(
                _(
                    "Your account has been deactivated. Please contact the administrator for further "
                    "assistance."
                )
            )

        attrs["user"] = user
        return super().validate(attrs)


class StudentSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    student_state = serializers.SerializerMethodField(read_only=True)
    college_state = serializers.SerializerMethodField(read_only=True)
    university = serializers.SerializerMethodField(read_only=True)
    college = serializers.SerializerMethodField(read_only=True)
    degree = serializers.SerializerMethodField(read_only=True)
    branch = serializers.SerializerMethodField(read_only=True)
    batch = serializers.SerializerMethodField(read_only=True)
    id_number = serializers.SerializerMethodField(read_only=True)
    student_ip_address_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ApplicationUser
        fields = (
            "id",
            "uuid",
            "fullname",
            "email",
            "phone",
            "address",
            "gender",
            "date_joined",
            "student_ip_address_data",
            "photo",
            "student_state",
            "college_state",
            "university",
            "college",
            "degree",
            "branch",
            "batch",
            "id_number",
        )

    def get_student_ip_address_data(self, obj):
        try:
            return obj.student_details.student_ip_address
        except:
            return ""

    def get_id_number(self, obj):
        return obj.student_details.id_number

    def get_batch(self, obj):
        try:
            return {
                "id": obj.student_details.batch.id,
                "year": f"{obj.batch.batches.start_year}-{obj.batch.batches.end_year}",
            }
        except:
            return {
                "id": obj.student_details.batch.id,
                "year": "",
            }

    def get_branch(self, obj):
        return {
            "id": obj.student_details.branch.id,
            "name": obj.student_details.branch.branch.name,
        }

    def get_degree(self, obj):
        return {
            "id": obj.student_details.degree.id,
            "name": obj.student_details.degree.degree.name,
        }

    def get_college(self, obj):
        return {
            "id": obj.student_details.college.id,
            "name": obj.student_details.college.name,
        }

    def get_university(self, obj):
        return {
            "id": obj.student_details.university.id,
            "name": obj.student_details.university.name,
        }

    def get_student_state(self, obj):
        return {
            "id": obj.student_details.student_state.id,
            "name": obj.student_details.student_state.name,
        }

    def get_college_state(self, obj):
        return {
            "id": obj.student_details.college_state.id,
            "name": obj.student_details.college_state.name,
        }

    def get_photo(self, obj):
        photo = obj.photo
        if not photo:
            return ""
        return UserPhotoSerializer(obj).data


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ["id", "meta_value"]


class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = ["id", "meta_value"]


class OurTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurTeam
        fields = ["id", "meta_value"]


class NecessitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Necessity
        fields = ["id", "meta_value"]


class AicteRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AicteRules
        fields = ["id", "meta_value"]


class ImplementationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Implementation
        fields = ["id", "meta_value"]


class ComplaintsMediaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    width = serializers.ReadOnlyField(source="width_photo", allow_null=True)
    height = serializers.ReadOnlyField(source="height_photo", allow_null=True)

    class Meta:
        model = ComplaintsMedia
        fields = ["id", "photo", "width", "height"]
        extra_kwargs = {"photo": {"required": True}}

    def create(self, validated_data):
        images = dict(self.context["request"].data)["photo"]
        if len(images) and images[0] == "":
            raise ValidationError(_("photo filed is required."))
        user = Complaints.objects.filter(
            id=self.context["view"].kwargs.get("nested_1_id")
        ).first()
        if not user:
            raise ValidationError(_("User not found"))
        bulk_images = [
            ComplaintsMedia(complaints=user, photo=images[i])
            for i in range(len(images))
        ]
        return ComplaintsMedia.objects.bulk_create(bulk_images)[0]


class ComplaintsSerializer(serializers.ModelSerializer):
    complaints_media = ComplaintsMediaSerializer(read_only=True, many=True)
    student_membership_id = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    allotted_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Complaints
        fields = [
            "id",
            "user",
            "issue",
            "complaint_number",
            "priority",
            "allotted_to",
            "status",
            "complaints_media",
            "resolution_provided",
            "upload_file",
            "create_time",
            "student_membership_id",
            "student_name",
            "allotted_to_name",
        ]
        extra_kwargs = {
            # "upload_file": {"required": True},
            "issue": {"required": True},
        }

    def get_student_membership_id(self, obj):
        try:
            return obj.user.student_details.student_membership_id
        except:
            return None

    def get_allotted_to_name(self, obj):
        try:
            return obj.allotted_to.user.fullname
        except:
            return None

    def get_student_name(self, obj):
        try:
            return obj.user.fullname
        except:
            return None

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get("user") or self.context.get("request").user
        validated_data["user"] = user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ApplicationUser
        fields = (
            "id",
            "username",
            "uuid",
            "email",
            "fullname",
            "phone",
            "gender",
            "address",
            "user_type",
            "password",
            "login_type",
            "is_active",
        )

    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)

        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user


class StudentDetailsSerializer(serializers.ModelSerializer):
    student = UserSerializer(many=False)
    photo = serializers.SerializerMethodField()
    student_state_data = serializers.SerializerMethodField(read_only=True)
    college_state_data = serializers.SerializerMethodField(read_only=True)
    university_data = serializers.SerializerMethodField(read_only=True)
    college_data = serializers.SerializerMethodField(read_only=True)
    degree_data = serializers.SerializerMethodField(read_only=True)
    branch_data = serializers.SerializerMethodField(read_only=True)
    batch_data = serializers.SerializerMethodField(read_only=True)
    total_cart_count = serializers.SerializerMethodField(read_only=True)
    is_notification = serializers.SerializerMethodField()

    class Meta:
        model = StudentDetails
        fields = [
            "id",
            "create_time",
            "student",
            "student_state",
            "college_state",
            "university",
            "college",
            "degree",
            "branch",
            "batch",
            "id_number",
            "student_membership_id",
            "photo",
            "student_state",
            "college_state",
            "university",
            "college",
            "degree",
            "branch",
            "batch",
            "deactivation_date",
            "is_active",
            "is_delete",
            "student_state_data",
            "college_state_data",
            "university_data",
            "college_data",
            "degree_data",
            "branch_data",
            "batch_data",
            "student_ip_address",
            "total_cart_count",
            "is_notification",
            "disable_date",
        ]
        read_only_fields = ("student_ip_address",)

    def update(self, instance, validated_data):
        student_data = validated_data.pop("student", {})
        student_instance = (
            instance.student
        )  # Access the 'student' field instead of 'user'

        # Update student_instance with the student_data
        for attr, value in student_data.items():
            setattr(student_instance, attr, value)

        # Save the student_instance
        student_instance.save()

        # Now update the remaining fields in the StudentDetails instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_is_notification(self, obj):
        try:
            user = obj.student
            # queryset = Notification.objects.filter(
            #     Q(receiver=user)
            #     | Q(is_public=True)
            #     | Q(group_of_student__in=[user], is_read=False)
            # )
            queryset = Notification.objects.filter(
                Q(receiver=user, is_read=False) |
                Q(group_of_student__in=[user], is_read=False)
            )

            return True if queryset.count() > 0 else False
        except Exception as e:
            print(e)
            return False

    def get_batch_data(self, obj):
        return {"id": obj.batch.id, "year": f"{obj.batch.batches.start_year}-{obj.batch.batches.end_year}"}

    def get_total_cart_count(self, obj):
        try:
            return Cart.objects.filter(user=obj.student, project__is_active=True).count()
        except:
            return ""

    def get_branch_data(self, obj):
        return {"id": obj.branch.id, "name": obj.branch.branch.name}

    def get_degree_data(self, obj):
        return {"id": obj.degree.id, "name": obj.degree.degree.name}

    def get_college_data(self, obj):
        return {"id": obj.college.id, "name": obj.college.name}

    def get_university_data(self, obj):
        return {"id": obj.university.id, "name": obj.university.name}

    def get_student_state_data(self, obj):
        return {"id": obj.student_state.id, "name": obj.student_state.name}

    def get_college_state_data(self, obj):
        return {"id": obj.college_state.id, "name": obj.college_state.name}

    def get_photo(self, obj):
        photo = obj.student.photo
        if not photo:
            return ""
        return UserPhotoSerializer(obj.student).data


class StudentChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    student_id = serializers.CharField(required=True)


class GrammarCheckSerializer(serializers.Serializer):
    grammar_check = serializers.CharField(max_length=1028)
