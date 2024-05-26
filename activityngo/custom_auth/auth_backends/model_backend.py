from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied


class CustomModelBackend(ModelBackend):
    def authenticate(
        self,
        request,
        username=None,
        email=None,
        phone=None,
        password=None,
        user_type=None,
        **kwargs
    ):
        UserModel = get_user_model()

        if "login_type" in kwargs and kwargs["login_type"] != "simple":
            try:
                user = UserModel.objects.get(
                    social_key=kwargs["social_key"],
                    login_type=kwargs["login_type"],
                    is_delete=False,
                )
                if not user.is_active:
                    raise PermissionDenied(_("User is not active"))
                return user
            except Exception:
                return None

        elif not username and not email and not phone:
            return None

        if username:
            email = username
            username = None

        username_query_dict = {"username__iexact": username}
        email_query_dict = {"email__iexact": email}
        phone_query_dict = {"phone": phone}

        try:
            query_filter = Q()
            if username:
                query_filter |= Q(**username_query_dict)
            if email:
                query_filter |= Q(**email_query_dict)
            if phone:
                query_filter |= Q(**phone_query_dict)

            if user_type:
                user = UserModel.objects.get(
                    query_filter, user_type=user_type, is_delete=False
                )
            else:
                user = UserModel.objects.get(query_filter, is_delete=False)

            if not user.is_active:
                raise PermissionDenied(_("User is not active."))

        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None
