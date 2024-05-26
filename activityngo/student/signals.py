from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from activityngo.student.models import StudentDetails


@receiver(post_save, sender=StudentDetails)
def set_deactivation_date(sender, instance, created, **kwargs):
    if created:
        user_profile = instance
        user_profile.deactivation_date = user_profile.create_time + timedelta(
            days=365 * 5
        )
        user_profile.save()
