from django.contrib import admin

from activityngo.ngo.models import (Directors, Franchise, Ngo, NgoCMS,
                                    Organization)


class DirectorsInline(admin.TabularInline):
    model = Directors
    extra = 1
    fieldsets = (
        (
            "Directors",
            {
                "fields": (
                    "organization",
                    "trustee_name",
                    "designation",
                    "director_no",
                    "pan_no",
                )
            },
        ),
    )
    verbose_name = "Directors Details"
    verbose_name_plural = "Directors Details"


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        DirectorsInline,
    ]
    fieldsets = (
        (
            "Organization",
            {
                "fields": (
                    "user",
                    "type",
                    "address",
                    "geo_tag",
                    "latitude",
                    "longitude",
                    "pan_no",
                    "tan_no",
                    "gstin",
                    "udhyam_aadhar_certificate_number",
                    "dpiit_certificate_number",
                    "llpin",
                    "website",
                    "no_of_directors",
                    "project_name",
                )
            },
        ),
    )
    list_display = ("id", "user", "type")

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)


class OrganizationInline(admin.TabularInline):
    model = Organization
    extra = 1
    fieldsets = (
        (
            "Organization",
            {
                "fields": (
                    "user",
                    "type",
                    "address",
                    "geo_tag",
                    "latitude",
                    "longitude",
                    "pan_no",
                    "tan_no",
                    "gstin",
                    "udhyam_aadhar_certificate_number",
                    "dpiit_certificate_number",
                    "llpin",
                    "website",
                    "no_of_directors",
                    "project_name",
                )
            },
        ),
    )
    verbose_name = "Organization Details"
    verbose_name_plural = "Organization Details"


@admin.register(Ngo)
class NgoAdmin(admin.ModelAdmin):
    # inlines = [DirectorsInline, ]
    fieldsets = (
        ("Ngo", {"fields": ("ngo_name", "franchise_code", "state", "university")}),
    )
    list_display = ("id", "ngo_name", "franchise_code")


admin.site.register(Franchise)
admin.site.register(Directors)
admin.site.register(NgoCMS)
