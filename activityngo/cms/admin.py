from django.contrib import admin

from activityngo.cms.models import CMS, FAQ, MyCartInstructions

# Register your models here.
admin.site.register(FAQ)
admin.site.register(CMS)
admin.site.register(MyCartInstructions)
