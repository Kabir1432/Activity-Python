from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from rest_framework.exceptions import ValidationError

from activityngo.custom_auth.models import BaseModel
from activityngo.discount.models import Discount
from activityngo.entities.models import ImplementationBatches
from activityngo.order.utils import (generate_invoice_number,
                                     student_invoice_generate)
from activityngo.project.models import Project  # ProjectPrice
from activityngo.utils.functions import generateRandomCode
from activityngo.utils.utils import get_order_invoice_path, get_activity_report_file_path, \
    get_student_qr_code_verification_filename, get_student_activity_certificate_file_filename, \
    get_student_activity_certificate_page_1_to_5_file_filename, get_student_activity_chapters_file_filename, \
    get_student_pie_chart_filename


class GSTCategory(BaseModel):
    description = models.TextField(_("order number"), blank=True, null=True)
    cgst_percentage = models.DecimalField(
        _("CGST percentage"), max_digits=5, decimal_places=2
    )
    sgst_percentage = models.DecimalField(
        _("SGST number"), max_digits=5, decimal_places=2
    )
    igst_percentage = models.DecimalField(
        _("IGST number"), max_digits=5, decimal_places=2
    )

    # def __str__(self):
    #     return self.description

    @property
    def total_gst_percentage(self):
        return self.cgst_percentage + self.sgst_percentage + self.igst_percentage


# Create your models here.
class Order(BaseModel):
    STATUS_PAYMENT = Choices(
        ("cancel", "Cancel"),
        ("pending", "Pending"),
        ("complete", "Complete"),
    )
    PAYMENT_METHOD = Choices(
        ("online", "Online"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="user_order",
    )
    order_number = models.CharField(
        _("order number"), max_length=20, null=True, unique=True
    )
    discount_code = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_discount_code"
    )
    discount_amount = models.DecimalField(
        _("Discount amount"), null=True, max_digits=10, decimal_places=2
    )
    gst_charges = models.DecimalField(
        _("GST charges"), null=True, max_digits=10, decimal_places=2, blank=True
    )
    sub_total_amount = models.DecimalField(
        _("Sub Total amount"), max_digits=10, decimal_places=2, default=0
    )
    total_amount = models.DecimalField(
        _("Total amount"), max_digits=10, decimal_places=2
    )
    status_of_payment = models.CharField(
        _("Status of payment"),
        max_length=10,
        choices=STATUS_PAYMENT,
        default=STATUS_PAYMENT.pending,
    )
    invoice_number = models.CharField(
        _(
            "Invoice number",
        ),
        max_length=50,
        null=True,
    )
    invoice_file = models.FileField(
        _("Invoice file"), upload_to=get_order_invoice_path, null=True
    )
    payment_via = models.CharField(
        _("Payment via"),
        choices=PAYMENT_METHOD,
        default=PAYMENT_METHOD.online,
        max_length=30,
    )
    payment_time = models.DateTimeField(_("Payment time"), null=True, blank=True)
    cgst = models.DecimalField(_("CGST"), max_digits=10, decimal_places=2, default=0)
    sgst = models.DecimalField(_("SGST"), max_digits=10, decimal_places=2, default=0)
    igst = models.DecimalField(_("IGST"), max_digits=10, decimal_places=2, default=0)
    payment_gateway_fee = models.DecimalField(_("Payment Gateway Fee"), max_digits=10, decimal_places=2, default=0)
    tax_service_fees = models.DecimalField(
        _("Tax service fees"), max_digits=10, decimal_places=2, default=0
    )
    is_temp_order = models.BooleanField(_("is temp order?"), default=True)
    android_payload = models.TextField(_('android_payload'), blank=True)
    webhook_payload = models.TextField(_('webhook payload'), blank=True)
    payment_id = models.CharField(_('payment id'), max_length=50, blank=True)
    is_webhook_call = models.BooleanField(_('is webhook call'), default=False)

    def save(self, *args, **kwargs):
        if not self.order_number:
            new_order_number = generateRandomCode(10)

            while self._meta.model._default_manager.filter(
                    order_number=new_order_number
            ).exists():
                new_order_number = generateRandomCode(10)

            self.order_number = new_order_number
        return super(Order, self).save(*args, **kwargs)


class OrderDetail(BaseModel):
    POINT = Choices(
        ("points_20", "20 Points"),
        ("points_10", "10 Points"),
        ("points_05", "05 Points"),
    )
    STATUS = Choices(
        ('incomplete', 'Incomplete'),  # this filed is for project is not complete
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('cancel', 'Cancel'),
        ('complete', 'Complete'),
        ('approve_complete', 'Approve Complete'),
    )
    order = models.ForeignKey(
        Order, related_name="order_details", on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="product_order_details"
    )

    number_of_points = models.CharField(
        max_length=10, choices=POINT, default=POINT.points_20
    )
    expire_on = models.DateTimeField(_("expire_on"), null=True)
    is_expire = models.BooleanField(_("is_expire"), default=False)
    is_complete = models.BooleanField(_("is complete"), default=False)
    activity_subscribed_date = models.DateTimeField(_('Activity subscribed date'), null=True)
    activity_completed_date = models.DateTimeField(_('Activity subscribed date'), null=True)
    activity_completed_date_by_student = models.DateTimeField(_('Activity subscribed date By student'), null=True)
    implementation_year = models.ForeignKey(
        ImplementationBatches, on_delete=models.SET_NULL, null=True, blank=True
    )
    number_of_days = models.PositiveIntegerField(_('Number of days'), null=True, blank=True)

    activity_status = models.CharField(_('Status'), choices=STATUS, max_length=30, default=STATUS.incomplete)
    report_file = models.FileField(
        _("Report File"), upload_to=get_activity_report_file_path, null=True
    )
    qr_code_verification = models.ImageField(
        upload_to=get_student_qr_code_verification_filename,
        null=True,
        blank=True,
    )
    student_activity_certificate_file = models.FileField(
        upload_to=get_student_activity_certificate_file_filename,
        null=True,
        blank=True,
    )
    student_activity_certificate_page_1_to_5_file = models.FileField(
        upload_to=get_student_activity_certificate_page_1_to_5_file_filename,
        null=True,
        blank=True,
    )
    student_activity_chapters = models.FileField(
        upload_to=get_student_activity_chapters_file_filename,
        null=True,
        blank=True,
    )
    report_generate_date = models.DateTimeField(_('Report generate date'), null=True, blank=True)
    student_activity_task_4 = models.FileField(
        upload_to=get_student_activity_chapters_file_filename,
        null=True,
        blank=True,
    )
    student_activity_task_9 = models.FileField(
        upload_to=get_student_activity_chapters_file_filename,
        null=True,
        blank=True,

    )
    student_activity_task_2_and_10 = models.FileField(
        upload_to=get_student_activity_chapters_file_filename,
        null=True,
        blank=True,

    )
    student_activity_short_report_chapter = models.FileField(
        upload_to=get_student_activity_chapters_file_filename,
        null=True,
        blank=True,
    )

    #     student activity pie chart

    student_activity_pie_chart_4 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_5 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_6 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_7 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_8 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_9 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_10 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_11 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_12 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_13 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_14 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_15 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_16 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_17 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_18 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )
    student_activity_pie_chart_19 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )

    student_activity_pie_chart_20 = models.ImageField(
        upload_to=get_student_pie_chart_filename,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        is_new_object = not self.pk  # Check if the object has a primary key
        if is_new_object:
            self.activity_subscribed_date = timezone.now()

        return super(OrderDetail, self).save(*args, **kwargs)
