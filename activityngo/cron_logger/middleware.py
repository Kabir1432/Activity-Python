import json
from activityngo.cron_logger.models import ServerErrorHandel


class ServerErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.captured_status_code = None

    def process_exception(self, request, exception):
        self.exception_data = {
            "error_name": type(exception).__name__,
            "error_message": str(exception),
        }

        # ServerErrorHandel.objects.create(error_name=error_name, error=error_message)
        return None

    def __call__(self, request):
        try:
            global response
            content_type = request.headers.get("Content-Type", "")
            if "application/json" in content_type:
                body_content = request.body.decode("utf-8")
                if body_content != "":
                    json_data = json.loads(body_content)
                    response = self.get_response(request)

                    if response.status_code == 500:
                        ServerErrorHandel.objects.create(
                            error_name=self.exception_data.get("error_name", None),
                            error=self.exception_data.get("error_message", None),
                            request_data=json_data,
                            request_path=request.path,
                            request_api=request.build_absolute_uri(),
                        )
                else:
                    response = self.get_response(request)
            elif "multipart/form-data" in content_type:
                body_content = request.POST.dict()
                if body_content != {}:
                    response = self.get_response(request)
                    if response.status_code == 500:
                        ServerErrorHandel.objects.create(
                            error_name=self.exception_data.get("error_name", None),
                            error=self.exception_data.get("error_message", None),
                            request_data=body_content,
                            request_path=request.path,
                            request_api=request.build_absolute_uri(),
                        )
            else:
                response = self.get_response(request)
            return response

        except:
            default_response = self.get_response(request)
            return default_response
