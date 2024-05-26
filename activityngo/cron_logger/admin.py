from django.contrib import admin

from activityngo.cron_logger.models import CronLogger, ServerErrorHandel


# Register your models here.
@admin.register(CronLogger)
class CronLoggerAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Cron Logger",
            {
                "fields": (
                    "create_time",
                    "cron_name",
                    "is_error",
                    "is_cron_complete_successfully",
                )
            },
        ),
    )
    list_display = (
        "create_time",
        "cron_name",
        "is_error",
        "is_cron_complete_successfully",
    )
    list_filter = (
        "cron_name",
        "is_error",
        "create_time",
        "is_cron_complete_successfully",
    )
    search_fields = (
        "cron_name",
        "is_error",
        "create_time",
        "is_cron_complete_successfully",
    )
    readonly_fields = ("create_time",)


admin.site.register(ServerErrorHandel)