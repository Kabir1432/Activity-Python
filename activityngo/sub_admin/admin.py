from django.contrib import admin

from activityngo.sub_admin.models import (CustomPermission, SubAdmin,
                                          UserAccessPermission,
                                          UserAdminAccessLog)

# Register your models here.
admin.site.register(SubAdmin)
admin.site.register(CustomPermission)
admin.site.register(UserAccessPermission)
admin.site.register(UserAdminAccessLog)
