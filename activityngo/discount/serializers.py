from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activityngo.custom_auth.models import ApplicationUser
from activityngo.custom_auth.serializers import BaseUserSerializer
from activityngo.discount.models import Discount, DiscountUsage
from activityngo.order.models import Order


class DiscountSerializer(serializers.ModelSerializer):
    # project_set = ProjectListSerializer(source="project", read_only=True, )
    user = serializers.PrimaryKeyRelatedField(
        queryset=ApplicationUser.objects.all(),
        many=True,
        read_only=False,
        # source='states'
    )
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = [
            "id",
            "is_active",
            "discount_name",
            "type_discount",
            "discount_price_project_type_20",
            "discount_price_project_type_10",
            "discount_price_project_type_05",
            "conjunction_discount",
            "usage_limit",
            "usage_limit_per_membership_id",
            "usage_limit_per_project_subscription",
            "active_date",
            "expire_date",
            "user",
            "current_discount_usage_count",
            "discount_limit_reached",
            # for batch discount
            "state",
            "college",
            "university",
            "degree",
            "branch",
            "batch",
            "user_data",
            "description",
            "code",
        ]
        extra_kwargs = {
            "users": {"required": False},
            "discount_name": {"required": True},
            "type_discount": {"required": True},
            "discount_price_project_type_20": {"required": True},
            "discount_price_project_type_10": {"required": True},
            "discount_price_project_type_05": {"required": True},
            "conjunction_discount": {"required": True},
            "usage_limit": {"required": True},
            "usage_limit_per_membership_id": {"required": True},
            "usage_limit_per_project_subscription": {"required": True},
            "active_date": {"required": True},
            "expire_date": {"required": True},
            "description": {"required": True},
        }

    def get_user_data(self, obj):
        try:
            user_data = [
                BaseUserSerializer(user_data).data for user_data in obj.user.all()
            ]
            return user_data
        except:
            return ""

    def validate(self, attrs):
        type_discount = attrs.get("type_discount")
        user = attrs.get("user")
        active_date = attrs.get("active_date")
        expire_date = attrs.get("expire_date")

        if type_discount == "individual_discount":
            if not user:
                raise ValidationError(_("For individual discounts, user is required."))
        elif type_discount == "batch_discount":
            required_fields = ["college", "university", "degree", "branch", "batch"]
            for field_name in required_fields:
                if not attrs.get(field_name):
                    raise ValidationError(
                        _(f"{field_name} is required for batch_discount")
                    )
        if active_date and expire_date and active_date >= expire_date:
            raise ValidationError(_("Active date must be less than expire date."))

        return super().validate(attrs)


class DiscountOrderSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_member_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "invoice_number", "student_name", "student_member_id"]

    def get_student_name(self, obj):
        try:
            return obj.user.fullname
        except:
            return ""

    def get_student_member_id(self, obj):
        try:
            return obj.user.student_details.student_membership_id
        except:
            return ""


class DiscountUsageSerializer(serializers.ModelSerializer):
    order_data = serializers.SerializerMethodField()

    class Meta:
        model = DiscountUsage
        fields = ["id", "user", "discount", "used_at", "order_data"]

    def get_order_data(self, obj):
        try:
            return DiscountOrderSerializer(
                Order.objects.filter(discount_code=obj.discount, user=obj.user),
                many=True,
                read_only=True,
            ).data
        except:
            return ""
