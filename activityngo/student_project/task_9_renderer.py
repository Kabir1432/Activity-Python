from rest_framework import status
from rest_framework.renderers import JSONRenderer

__all__ = ["SubmitTask9Renderer"]


class SubmitTask9Renderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = data

        if status.is_server_error(status_code) or status.is_client_error(status_code):
            try:
                error_dict = next(iter(data.items()))
                category = error_dict[0]

                if category in ["short_question", "dropdown_question", "numeric_question",
                                "percentage_question"] and isinstance(error_dict[1], dict):
                    index_of = next(iter(error_dict[1]))
                    errors = "".join(
                        error_dict[1][index_of][next(iter(error_dict[1][index_of]))][0]
                    )
                    field_name = next(iter(error_dict[1][index_of]))

                    if errors.find("This field is required.") != -1:
                        errors = f"{field_name} field required in {category} at {index_of}."
                    else:
                        errors = errors.replace(".", "") + f" in {category} at {index_of}."

                else:
                    errors = "".join(iter(error_dict[1]))

                    if errors.find("This field is required.") != -1:
                        errors = f'{category}{errors.replace("This", "")}'

            except Exception as e:
                filtered_data = [item for item in data if bool(item)]
                errors = filtered_data[0].get('non_field_errors')[0]

            response = {"errors": errors}

        return super(SubmitTask9Renderer, self).render(
            response, accepted_media_type, renderer_context
        )
