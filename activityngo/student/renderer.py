from rest_framework import status
from rest_framework.renderers import JSONRenderer


class StudentRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = data
        if status.is_server_error(status_code) or status.is_client_error(status_code):
            try:
                error_dict = next(iter((data.items())))
                if "student" in error_dict and isinstance(error_dict[1], dict):
                    errors = "".join(error_dict[1].get(next(iter(error_dict[1])))[0])
                    if errors.find("This field is required.") != -1:
                        errors = (
                            f"{next(iter(error_dict[1]))} field required in student."
                        )
                    else:
                        errors = errors.replace(".", "") + " in student."
                else:
                    error_dict = next(iter((data.items())))
                    errors = "".join(iter(error_dict[1]))

                    if errors.find("This field is required.") != -1:
                        errors = f'{error_dict[0]}{errors.replace("This", "")}'
            except:
                errors = data[0]

            response = {"errors": errors}
        return super(StudentRenderer, self).render(
            response, accepted_media_type, renderer_context
        )
