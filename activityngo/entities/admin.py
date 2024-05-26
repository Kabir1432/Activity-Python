from django.contrib import admin

from activityngo.entities.models import (Batches, Branch, Degree,
                                         ProjectCategory, ProjectType, State, ImplementationBatches)

# Register your models here.
admin.site.register(State)
admin.site.register(Degree)
admin.site.register(Branch)
admin.site.register(Batches)
admin.site.register(ImplementationBatches)
admin.site.register(ProjectCategory)
admin.site.register(ProjectType)
# admin.site.register(ProjectCategory)
# admin.site.register(ProjectCategory)
# admin.site.register(ProjectCategory)
