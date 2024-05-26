import django_filters
from django_filters import rest_framework as filters

from activityngo.custom_auth.models import ApplicationUser


class UserFilter(filters.FilterSet):
    class Meta:
        model = ApplicationUser
        fields = {
            "user_type": ["in", "exact"],
        }
