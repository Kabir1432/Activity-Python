from django.contrib import admin

from activityngo.website_content.models import WebsiteContent, WebsiteCoverPhoto

# Register your models here.
admin.site.register(WebsiteContent)
admin.site.register(WebsiteCoverPhoto)