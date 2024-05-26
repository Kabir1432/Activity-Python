from rest_framework.authentication import TokenAuthentication

from activityngo.custom_auth.models import MultiToken


class MultiTokenAuthentication(TokenAuthentication):
    model = MultiToken
