from django.contrib import admin

from activityngo.order.models import Order, OrderDetail


# Register your models here.
# admin.site.register(Order)


class OrderDetailAdmin(OrderDetail):
    class Meta:
        proxy = True


@admin.register(OrderDetailAdmin)
class OrderDetailAdmin(admin.ModelAdmin):
    # inlines = [CustomerShippingAddressBranchInline, ]
    fieldsets = (
        (
            "OrderDetailAdmin",
            {
                "fields": (
                    "order",
                    "project",
                    "number_of_points",
                    "expire_on",
                    "is_expire",
                    "is_complete",
                    "activity_subscribed_date",
                    "activity_completed_date",
                    "activity_completed_date_by_student",
                    "activity_status",
                    "report_file",
                    "qr_code_verification",
                    "student_activity_certificate_file",
                    "student_activity_certificate_page_1_to_5_file",
                    "student_activity_chapters",
                    "report_generate_date",
                    "student_activity_task_4",
                    "student_activity_task_9",
                    "student_activity_task_2_and_10",
                    "student_activity_short_report_chapter",
                    "student_activity_pie_chart_4",
                    "student_activity_pie_chart_5",
                    "student_activity_pie_chart_6",
                    "student_activity_pie_chart_7",
                    "student_activity_pie_chart_8",
                    "student_activity_pie_chart_9",
                    "student_activity_pie_chart_10",
                    "student_activity_pie_chart_11",
                    "student_activity_pie_chart_12",
                    "student_activity_pie_chart_13",
                    "student_activity_pie_chart_14",
                    "student_activity_pie_chart_15",
                    "student_activity_pie_chart_16",
                    "student_activity_pie_chart_17",
                    "student_activity_pie_chart_18",
                    "student_activity_pie_chart_19",
                    "student_activity_pie_chart_20",
                )
            },
        ),
    )

    # list_display = ('fullname', 'phone', 'company_name', 'is_active', 'viewResult')


# from django.contrib import admin

class OrderDetailAdminInline(admin.TabularInline):
    model = OrderDetail
    # inlines = [CustomerShippingAddressBranchInline, ]
    fieldsets = (
        (
            "OrderDetail",
            {
                "fields": (
                    "order",
                    "project",
                    "number_of_points",
                    "expire_on",
                    "is_expire",
                    "is_complete",
                    "activity_status",
                    "report_file",
                    "qr_code_verification",
                    "student_activity_certificate_file",
                    "student_activity_certificate_page_1_to_5_file",
                    "student_activity_chapters",
                    "report_generate_date",
                    "student_activity_task_4",
                    "student_activity_task_9",
                    "student_activity_task_2_and_10",
                    "student_activity_short_report_chapter",
                    "student_activity_pie_chart_4",
                    "student_activity_pie_chart_5",
                    "student_activity_pie_chart_6",
                    "student_activity_pie_chart_7",
                    "student_activity_pie_chart_8",
                    "student_activity_pie_chart_9",
                    "student_activity_pie_chart_10",
                    "student_activity_pie_chart_11",
                    "student_activity_pie_chart_12",
                    "student_activity_pie_chart_13",
                    "student_activity_pie_chart_14",
                    "student_activity_pie_chart_15",
                    "student_activity_pie_chart_16",
                    "student_activity_pie_chart_17",
                    "student_activity_pie_chart_18",
                    "student_activity_pie_chart_19",
                    "student_activity_pie_chart_20",
                )
            },
        ),
    )

    # list_display = ('fullname', 'phone', 'company_name', 'is_active', 'viewResult')


@admin.register(Order)
class OrderActionAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Order Action",
         {"fields": (
             'user', 'order_number', 'discount_code', 'discount_amount', 'gst_charges', 'total_amount',
             'status_of_payment', 'invoice_number', 'invoice_file', 'payment_via', 'payment_time', 'cgst', 'sgst',
             'igst', 'tax_service_fees', 'is_temp_order', 'android_payload', 'webhook_payload', 'payment_id',
             'is_webhook_call')}),

    )
    list_display = ('order_number', 'user', 'total_amount')
    # list_display_links = None
    sortable_by = ()
    inlines = (OrderDetailAdminInline,)
