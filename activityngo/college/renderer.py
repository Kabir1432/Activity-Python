from rest_framework import status
from rest_framework.renderers import JSONRenderer

__all__ = ["CollegeUserRenderer"]


class CollegeUserRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = data
        if status.is_server_error(status_code) or status.is_client_error(status_code):
            try:
                error_dict = next(iter((data.items())))
                if "user_details" in error_dict and isinstance(error_dict[1], dict):
                    errors = "".join(error_dict[1].get(next(iter(error_dict[1])))[0])
                    if errors.find("This field is required.") != -1:
                        errors = (
                            f"{next(iter(error_dict[1]))} field required in user_data."
                        )
                    else:
                        errors = errors.replace(".", "") + " in user_data."
                else:
                    error_dict = next(iter((data.items())))
                    errors = "".join(iter(error_dict[1]))

                    if errors.find("This field is required.") != -1:
                        errors = f'{error_dict[0]}{errors.replace("This", "")}'
            except:
                errors = data[0]

            response = {"errors": errors}
        return super(CollegeUserRenderer, self).render(
            response, accepted_media_type, renderer_context
        )


class CollegeBatchesRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = data
        if status.is_server_error(status_code) or status.is_client_error(status_code):
            try:
                error_dict = next(iter((data.items())))
                if "college_batches" in error_dict and isinstance(error_dict[1], dict):
                    errors = "".join(error_dict[1].get(next(iter(error_dict[1])))[0])
                    if errors.find("This field is required.") != -1:
                        errors = f"{next(iter(error_dict[1]))} field required in college_batches."
                    else:
                        errors = errors.replace(".", "") + " in college_batches."
                else:
                    error_dict = next(iter((data.items())))
                    errors = "".join(iter(error_dict[1]))

                    if errors.find("This field is required.") != -1:
                        errors = f'{error_dict[0]}{errors.replace("This", "")}'
            except:
                errors = data[0]

            response = {"errors": errors}
        return super(CollegeBatchesRenderer, self).render(
            response, accepted_media_type, renderer_context
        )
