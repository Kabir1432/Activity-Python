# access_logs/middleware.py
from .models import UserAdminAccessLog


class AccessLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and (
            request.user.user_type == "student" or request.user.user_type == "sub_admin"
        ):
            model_name, method_name = self.get_model_and_method(request)

            if model_name and method_name:
                actions = {
                    "POST": (201, "created"),
                    "PUT": (200, "updated"),
                    "PATCH": (200, "updated"),
                    "GET": (200, "view"),
                    "DELETE": (204, "deleted"),
                }
                status_code, action_text = actions.get(request.method, (None, None))
                try:
                    if status_code is not None and response.status_code == status_code:
                        final_msg = f"{request.user.fullname} {action_text} {model_name}"
                        UserAdminAccessLog.objects.create(
                            user=request.user,
                            action=final_msg,
                            model_name=model_name,
                        )
                except:
                    pass
        return response

    def get_model_and_method(self, request):
        view = request.resolver_match.func

        # Extract model name from the view class's queryset attribute
        if (
            hasattr(view.cls, "queryset")
            and view.cls.queryset
            and hasattr(view.cls.queryset.model, "__name__")
        ):
            model_name = view.cls.queryset.model.__name__
        else:
            model_name = None

        # Extract HTTP method
        method_name = request.method

        return model_name, method_name
