from decimal import Decimal
from django.db import transaction
from django.db.models import Case, DecimalField, ExpressionWrapper, F, Sum, Value, When, IntegerField
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from num2words import num2words
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.views import APIView
from activityngo.cart.models import Cart
from activityngo.cron_logger.models import ServerErrorHandel
from activityngo.discount.models import DiscountUsage
from activityngo.order.models import GSTCategory, Order, OrderDetail
from activityngo.order.serializers import (
    GSTCategorySerializer,
    OrderSerializer,
    OrderDetailsSerializer,
    RazorPaySerializer, GenerateReport, SendReportSerializer,
)
from activityngo.utils.permissions import IsAPIKEYAuthenticated, IsStudentUser
from rest_framework.response import Response
import razorpay
from django.conf import settings
from rest_framework.exceptions import NotFound, ValidationError
from .tasks import generate_report
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.utils import timezone
from ..entities.models import ImplementationBatches
from ..utils.sendgrid_email_send import send_activity_report_email, send_order_invoice_email
from activityngo.order.utils import generate_invoice_number
from activityngo.order.utils import student_invoice_generate

class GSTCategoryViewSet(viewsets.ModelViewSet):
    queryset = GSTCategory.objects.all()
    serializer_class = GSTCategorySerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['user', 'is_temp_order']
    search_fields = (
        "user__email",
        "user__student_details__student_membership_id",
        "user__phone",
    )

    def get_permissions(self):
        if self.action == "create":
            # Use the custom permission class for creating orders
            return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsStudentUser()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.user_type == "student":
            recent_purchase = self.request.query_params.get("recent_purchase")
            queryset = queryset.filter(is_temp_order=False)
            if recent_purchase:
                if recent_purchase.lower() in ["1", "true"]:
                    return queryset.order_by("-create_time")[:5]
            return queryset.filter(user=user).order_by("-create_time")
        return queryset.order_by("-create_time")

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        user = self.request.user
        if user.user_type == "student":
            recent_purchase = self.request.query_params.get("recent_purchase")
            if recent_purchase:
                point_conversion = Case(
                    When(number_of_points='points_20', then=Value(20)),
                    When(number_of_points='points_10', then=Value(10)),
                    When(number_of_points='points_05', then=Value(5)),
                    output_field=IntegerField()
                )
                total_points = OrderDetail.objects.filter(order__user=user, order__is_temp_order=False).aggregate(
                    total_points=Sum(point_conversion)
                )['total_points']
                dashboard_count = {
                    "no_of_projects_purchased": OrderDetail.objects.filter(
                        order__user=user, order__is_temp_order=False, is_delete=False
                    ).count(),
                    "total_points_purchased": total_points if total_points else 0

                    ,
                    "yet_to_complete_projects": OrderDetail.objects.filter(
                        order__user=user, order__is_temp_order=False, is_delete=False, is_complete=False,
                        is_expire=False
                    ).count(),
                    "completed_projects": OrderDetail.objects.filter(
                        order__user=user, order__is_temp_order=False, is_delete=False, is_complete=True
                    ).count(),
                }
                response.data.update(dashboard_count)
        return response


class RazorPayViewSet(APIView):
    permission_classes = []

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = RazorPaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = request.data.get("order_id")
        android_payload = request.data.get("razorpay_signature")

        try:
            data = Order.objects.get(pk=order_id)
            data.android_payload = android_payload
            data.save()
        except Order.DoesNotExist:
            # Handle the case where the order with the specified ID does not exist
            return Response(
                {"error": "Order does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def razorpay_webhook_api(request):
    if request.method == 'POST':
        # Verify the webhook signature
        try:
            razorpay_api_key = settings.RAZOR_PAY_API_KEY
            razorpay_webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET

            # Create a Razorpay client with your API key
            client = razorpay.Client(auth=(razorpay_api_key, ''))

            # Verify the webhook signature using the webhook secret

            client.utility.verify_webhook_signature(
                request.body.decode('utf-8'),
                request.headers['X-Razorpay-Signature'],
                razorpay_webhook_secret
            )
        except razorpay.errors.SignatureVerificationError as e:
            # Webhook signature verification failed
            ServerErrorHandel.objects.create(error_name="error in razor pay", error=e,
                                             request_data=request.data)
            return Response({"status": "ok"}, status=status.HTTP_200_OK)

        # Webhook signature verification successful
        payload = request.data  # Assuming the payload is sent as JSON in the request body
        event_type = payload.get('event', '')
        try:
            order_id = payload.get('payload').get('payment').get('entity').get('notes').get('main_order_id')
            data = Order.objects.get(pk=order_id)
            data.webhook_payload = f"{payload}"
            if event_type == 'payment.captured' and not data.is_webhook_call:
                cart = Cart.objects.filter(user=data.user)
                cart.delete()
                data.is_temp_order = False
                data.is_webhook_call = True
                data.status_of_payment = "complete"
                number = generate_invoice_number()
                if not data.invoice_number and number:
                    data.invoice_number = number
                if data.discount_code:
                    DiscountUsage.objects.create(
                        user=data.user, discount=data.discount_code
                    )
                    obj = data.discount_code
                    obj.current_discount_usage_count += 1
                    obj.save()
                data.save()
                student_invoice_generate(data.id)
                data = Order.objects.get(pk=order_id)
                send_order_invoice_email(data)
            data.payment_id = payload.get('payload').get('payment').get('entity').get('id')
            data.save()
            # student_invoice_generate(data.id)
            # send_order_invoice_email(data)
            # if event_type == 'payment.captured' and not data.is_webhook_call:

        except Exception as e:
            ServerErrorHandel.objects.create(error_name="error in razor pay", error=e,
                                             request_data=request.data)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    else:
        # Handle non-POST requests if needed
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


def student_order(request, id):
    order_data = Order.objects.prefetch_related("order_details").get(pk=id)
    total_tax_per = GSTCategory.objects.first().total_gst_percentage
    gst_data = GSTCategory.objects.first()
    point_to_field_mapping = {
        "points_20": "price_of_20_point",
        "points_10": "price_of_10_point",
        "points_05": "price_of_05_point",
    }

    # Annotate the OrderDetail queryset with total_price and total_tax_amount
    order_details = order_data.order_details.annotate(
        total_price=Case(
            *[
                When(number_of_points=point, then=F("project__" + field_name))
                for point, field_name in point_to_field_mapping.items()
            ],
            default=Value(0),  # Default value if number_of_points value not found
            output_field=DecimalField(
                max_digits=10, decimal_places=2
            ),  # Specify DecimalField as output_field
        ),
        order_tax_amount=ExpressionWrapper(
            F("total_price") * Decimal(str(total_tax_per)) / 100 + F("total_price"),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
        tax_amount=ExpressionWrapper(
            F("total_price") * Decimal(str(total_tax_per)) / 100 + F("total_price"),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
    )
    total_tax = order_details.aggregate(total_tax=Sum("tax_amount")).get("total_tax")
    total_project_price = order_details.aggregate(
        total_project_price=Sum("total_price")
    ).get("total_project_price")
    amount_in_words = num2words(order_data.total_amount).capitalize()
    data = {
        "order_data": order_data,
        "order_details": order_details,
        "total_tax": total_tax,
        "total_project_price": total_project_price,
        "gst_data": gst_data,
        "amount_in_words": amount_in_words,
        "order_details_count": order_data.order_details.all().count(),
    }
    return render(request, "report/student_order_invoice.html", data)


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['order__user', 'order__is_temp_order']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.user_type == "student":
            return queryset.filter(order__is_temp_order=False, order__user=user).order_by("-create_time")
            # return queryset.filter(user=user)
        return queryset.order_by("-create_time")


class GetCompleteProjectListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['number_of_points', 'activity_status']
    search_fields = (
        "order__invoice_number",
        "order__user__student_details__student_membership_id",
    )
    ordering_fields = [
        "order__user__student_details__student_membership_id",
        "project__title",
        "create_time",
        "activity_completed_date_by_student",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_complete=True)
        activity_status_list = self.request.query_params.get('activity_status__in')
        if activity_status_list:
            queryset = queryset.filter(activity_status__in=activity_status_list.split(','))
        return queryset.order_by("-create_time")


class GenerateReportAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GenerateReport(data=request.data)
        if serializer.is_valid():
            order_detail_obj = OrderDetail.objects.get(pk=serializer.data.get('order_id'))
            order_detail_obj.activity_status = "processing"
            order_detail_obj.implementation_year = ImplementationBatches.objects.get(
                pk=serializer.data.get('implementation_batch'))
            order_detail_obj.number_of_days = serializer.data.get('number_of_days')
            order_detail_obj.activity_subscribed_date = serializer.data.get('activity_subscribed_date')
            order_detail_obj.activity_completed_date = serializer.data.get('expire_on')
            order_detail_obj.report_generate_date = timezone.now()

            order_detail_obj.save()
            # generate_report(serializer.data.get('order_id'), request.data)
            generate_report.delay(serializer.data.get('order_id'), request.data)
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendReportAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendReportSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order_detail_obj = OrderDetail.objects.get(pk=serializer.data.get('order_id'),
                                                           )
            except OrderDetail.DoesNotExist:
                raise NotFound(detail="Order Detail not found")

            if order_detail_obj.report_file and (
                    order_detail_obj.activity_status == "approve_complete" or order_detail_obj.activity_status == "complete"):
                send_activity_report_email(order_detail_obj.order.user.email, order_detail_obj)
                return Response({"data": "Report sent successfully on your registered Email"},
                                status=status.HTTP_201_CREATED)
            raise ValidationError(detail="Report not generated. Contact with Admin")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
