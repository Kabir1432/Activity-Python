from django.utils import timezone

from activityngo.cron_logger.models import CronLogger
from activityngo.custom_auth.models import ApplicationUser
from activityngo.student.models import StudentDetails


def inactive_student_after_1_year():
    try:
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        inactive_users = ApplicationUser.objects.filter(
            user_type="student", last_login__lt=one_year_ago
        )

        for user in inactive_users:
            user.is_active = False
            user.save()
        CronLogger.objects.create(
            cron_name="inactive_student_after_1_year",
            is_error=f"Cron complete successfully inactive_users:-->{inactive_users}",
            is_cron_complete_successfully=True,
        )
    except Exception as e:
        CronLogger.objects.create(
            cron_name="inactive_student_after_1_year",
            is_error=e,
            is_cron_complete_successfully=False,
        )


def inactive_5_year_old_student():
    try:
        current_date = timezone.now()
        student_to_deactivate = StudentDetails.objects.filter(
            deactivation_date__lte=current_date
        )

        for student_profile in student_to_deactivate:
            student_profile.student.is_active = False
            student_profile.student.save()

        CronLogger.objects.create(
            cron_name="inactive_5_year_old_student",
            is_error=f"Cron complete successfully student_to_deactivate:-->{student_to_deactivate.count()}",
            is_cron_complete_successfully=True,
        )
    except Exception as e:
        CronLogger.objects.create(
            cron_name="inactive_5_year_old_student",
            is_error=e,
            is_cron_complete_successfully=False,
        )
