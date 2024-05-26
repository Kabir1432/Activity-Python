import razorpay
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
from activityngo.cart.models import Cart
from activityngo.custom_auth.serializers import BaseUserSerializer
from activityngo.discount.models import DiscountUsage
from activityngo.entities.models import ImplementationBatches
from activityngo.order.models import GSTCategory, Order, OrderDetail
from activityngo.order.utils import set_expire_days, student_invoice_generate
from activityngo.project.models import Project
from activityngo.project.serializers import ProjectListSerializer
from activityngo.student.serializer import StudentDetailsSerializer
from activityngo.student_project.models import StudentTaskStatus
from activityngo.task_evaluation.serializers import EvaluationResultSerializer


class GSTCategorySerializer(serializers.ModelSerializer):
    # project_set = ProjectListSerializer(source="project", read_only=True, )
    total_gst_percentage = serializers.ReadOnlyField()

    class Meta:
        model = GSTCategory
        fields = [
            "id",
            "description",
            "cgst_percentage",
            "sgst_percentage",
            "igst_percentage",
            "total_gst_percentage",
        ]
        extra_kwargs = {
            "cgst_percentage": {"required": True},
            "sgst_percentage": {"required": True},
            "igst_percentage": {"required": True},
        }

    def validate(self, data):
        cgst_percentage = data.get("cgst_percentage")
        sgst_percentage = data.get("sgst_percentage")
        igst_percentage = data.get("igst_percentage")

        if cgst_percentage < 0 or sgst_percentage < 0 or igst_percentage < 0:
            raise serializers.ValidationError("Percentage values must be 0 or greater.")
        return data

    def create(self, request, *args, **kwargs):
        # Check if a GSTCategory instance already exists
        existing_instance = GSTCategory.objects.first()
        if existing_instance:
            raise ValidationError(_("Only one GSTCategory instance is allowed."))

        return super().create(request, *args, **kwargs)


class OrderDetailsSerializer(serializers.ModelSerializer):
    # product_name = serializers.SerializerMethodField()
    purchased_project_category = serializers.SerializerMethodField()
    purchased_project_name = serializers.SerializerMethodField()
    selected_franchisee_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    project_details = serializers.SerializerMethodField()
    evaluation_data = serializers.SerializerMethodField()
    expire_on = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    student_details = serializers.SerializerMethodField()
    number_of_days = serializers.SerializerMethodField()

    # project_details = ProjectListSerializer(source="product_order_details", read_only=True)

    class Meta:
        model = OrderDetail
        fields = (
            "id",
            "is_active",
            "create_time",
            "order",
            "selected_franchisee_name",
            "project",
            "number_of_points",
            "expire_on",
            "is_expire",
            "activity_subscribed_date",
            "report_file",
            "number_of_days",
            "activity_completed_date_by_student",
            "activity_completed_date",
            "purchased_project_category",
            "create_time",
            "purchased_project_name",
            "full_name",
            "student_id",
            "project_details",
            "evaluation_data",
            "activity_status",
            "student_details",

        )

    def get_student_details(self, obj):
        try:
            return StudentDetailsSerializer(obj.order.user.student_details, many=False).data
        except:
            return ""

    def get_number_of_days(self, obj):
        try:
            return obj.project.minimum_number_of_days
        except:
            return ""


    # def get_expire_on(self, obj):
    #     try:
    #         expire_on = obj.expire_on.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    #         return expire_on
    #     except:
    #         return ""

    def get_project_details(self, obj):
        try:
            return ProjectListSerializer(Project.objects.filter(pk=obj.project.id).first(), read_only=True).data
        except:
            return ""

    def get_evaluation_data(self, obj):
        try:
            return EvaluationResultSerializer(obj, read_only=True).data
        except:
            return ""

    def get_full_name(self, obj):
        try:
            return obj.order.user.fullname
        except:
            return ""

    def get_student_id(self, obj):
        try:
            return obj.order.user.student_details.student_membership_id
        except:
            return ""

    def get_purchased_project_category(self, obj):
        try:
            return obj.project.category.name
        except:
            return ""

    def get_purchased_project_name(self, obj):
        try:
            return obj.project.title
        except:
            return ""

    def get_selected_franchisee_name(self, obj):
        try:
            return obj.project.franchise_ngo_name.ngo_name
        except:
            return ""


class OrderSerializer(serializers.ModelSerializer):
    order_data = OrderDetailsSerializer(
        source="order_details", many=True, read_only=True
    )
    student_data = serializers.SerializerMethodField()
    discount_code_data = serializers.SerializerMethodField()

    # project_set = ProjectListSerializer(source="project", read_only=True, )

    class Meta:
        model = Order
        fields = [
            "id",
            "create_time",
            "user",
            "order_number",
            "discount_code",
            "discount_code_data",
            "discount_amount",
            "gst_charges",
            "total_amount",
            "status_of_payment",
            "invoice_number",
            "student_data",
            "order_data",
            "invoice_file",
            "payment_via",
            "payment_time",
            "cgst",
            "sgst",
            "igst",
            "tax_service_fees",
            "payment_id",
            "sub_total_amount",
            "payment_gateway_fee",
        ]
        extra_kwargs = {
            # 'user': {'required': True},
            # 'discount_code': {'required': True},
            "discount_amount": {"required": True},
            # 'gst_charges': {'required': True},
            "total_amount": {"required": True},
            "cgst": {"required": True},
            "sgst": {"required": True},
            "igst": {"required": True},
            "tax_service_fees": {"required": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        additional_data = getattr(self, 'razor_pay_details', {})

        representation["api_key"] = additional_data.get('api_key')
        representation["order_id"] = additional_data.get('order_id')

        return representation

    def get_student_data(self, obj):
        try:
            return StudentDetailsSerializer(obj.user.student_details, many=False).data
        except:
            return ""

    def get_discount_code_data(self, obj):
        try:
            return obj.discount_code.discount_name
        except:
            return ""

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get("user") or self.context.get("request").user
        validated_data["user"] = user
        cart = Cart.objects.filter(user=user, project__is_active=True)
        if not cart:
            raise ValidationError(_("Cart is empty."))
        if 1 > validated_data.get('total_amount'):
            raise ValidationError(_("Cart value must be greater than Rs 1."))
        data = super().create(validated_data)
        for cart_items in cart:
            # days = (
            #     cart_items.project.days_of_20_point
            #     if cart_items.number_of_points == "points_20"
            #     else cart_items.project.days_of_10_point
            #     if cart_items.number_of_points == "points_10"
            #     else cart_items.project.days_of_05_point
            # )
            days = cart_items.project.expire_duration_in_days_by_students
            order_details = OrderDetail.objects.create(
                order=data,
                project=cart_items.project,
                number_of_points=cart_items.number_of_points,
                expire_on=set_expire_days(days),
            )
            StudentTaskStatus.objects.create(
                order_details=order_details,
                task1="not_submitted",
                task2="not_submitted",
                task3="not_submitted",
                task4="not_submitted",
                task5="not_applicable"
                if cart_items.number_of_points == "points_05"
                else "not_submitted",
                task6="not_applicable"
                if cart_items.number_of_points == "points_05"
                else "not_submitted",
                task7="not_submitted"
                if cart_items.number_of_points == "points_20"
                else "not_applicable",
                task8="not_submitted"
                if cart_items.number_of_points == "points_20"
                else "not_applicable",
                task9="not_submitted"
                if cart_items.number_of_points == "points_20"
                else "not_applicable",
                task10="not_submitted"
                if cart_items.number_of_points == "points_20"
                else "not_applicable",
            )
        # cart.delete()

        if data.discount_code:
            # Check if total used discount reached or not
            total_allowed_discount_usage = data.discount_code.usage_limit
            current_discount_usage_count = DiscountUsage.objects.filter(
                discount=data.discount_code
            ).count()
            if current_discount_usage_count >= total_allowed_discount_usage:
                raise ValidationError(_("Discount has reached its total usage limit ."))
            # Check if total used discount reached or not for user limit
            total_allowed_discount_for_user_usage = (
                data.discount_code.usage_limit_per_membership_id
            )
            current_discount_usage_by_discount_count = DiscountUsage.objects.filter(
                discount=data.discount_code, user=user
            ).count()
            if (
                    current_discount_usage_by_discount_count
                    >= total_allowed_discount_for_user_usage
            ):
                raise ValidationError(_("Discount has reached its total usage limit ."))
        # try:
        # this code need to add after payment Done
        # if data.discount_code:
        #     DiscountUsage.objects.create(user=data.user, discount=data.discount_code)
        #     obj = data.discount_code
        #     obj.current_discount_usage_count += 1
        #     obj.save()

        amount = int(data.total_amount) * 100
        api_key = settings.RAZOR_PAY_API_KEY

        client = razorpay.Client(auth=(settings.RAZOR_PAY_API_KEY, settings.KEY_SECRET))

        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': 'receipt_order_1',
            'payment_capture': 1,
            'notes': {
                'main_order_id': data.id,
            }
        }

        order = client.order.create(data=payment_data)

        razor_pay_details_dict = {
            'api_key': api_key,
            'order_id': order['id']
        }

        self.razor_pay_details = razor_pay_details_dict
        # student_invoice_generate(data.id)
        return data


class RazorPaySerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    # razor_pay_order_id = serializers.CharField(required=True)
    # razorpay_payment_id = serializers.CharField(required=True)
    # razorpay_signature = serializers.CharField(required=True)
    android_payload = serializers.CharField(required=True)


class GenerateReport(serializers.Serializer):
    implementation_batch = serializers.PrimaryKeyRelatedField(queryset=ImplementationBatches.objects.all())
    order_id = serializers.PrimaryKeyRelatedField(queryset=OrderDetail.objects.all())
    number_of_days = serializers.IntegerField(min_value=1, max_value=150)
    activity_subscribed_date = serializers.DateTimeField()
    expire_on = serializers.DateTimeField()



class SendReportSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
