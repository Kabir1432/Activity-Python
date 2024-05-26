from django.db.models.signals import post_save
from django.dispatch import receiver

from activityngo.sub_admin.models import (CustomPermission, SubAdmin,
                                          UserAccessPermission)


@receiver(post_save, sender=SubAdmin)
def update_order_status(sender, instance, created, **kwargs):
    if created:
        permissions = CustomPermission.objects.all()
        user_access_permission = [
            UserAccessPermission(user=instance.user, custom_permission=permission)
            for permission in permissions
        ]

        UserAccessPermission.objects.bulk_create(user_access_permission)


@receiver(post_save, sender=CustomPermission)
def update_order_status(sender, instance, created, **kwargs):
    if created:
        user_list = SubAdmin.objects.all()
        user_access_permission = [
            UserAccessPermission(user=user.user, custom_permission=instance)
            for user in user_list
        ]

        UserAccessPermission.objects.bulk_create(user_access_permission)
