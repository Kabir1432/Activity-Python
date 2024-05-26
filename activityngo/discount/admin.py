from django.contrib import admin

from activityngo.discount.models import Discount, DiscountUsage

# Register your models here.
admin.site.register(Discount)
admin.site.register(DiscountUsage)
