from django.contrib import admin

from activityngo.college.models import (
    BranchBatches,
    College,
    CollegeCMS,
    CollegeDegree,
    CollegeUsers,
    DegreeBranch,
)

# Register your models here.
admin.site.register(College)
admin.site.register(CollegeDegree)
admin.site.register(DegreeBranch)
admin.site.register(BranchBatches)
admin.site.register(CollegeUsers)
admin.site.register(CollegeCMS)
