from rest_framework import status
from rest_framework.renderers import JSONRenderer

__all__ = ["DynamicRejectedQuestionRenderer"]


class DynamicRejectedQuestionRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = data

        if status.is_server_error(status_code) or status.is_client_error(status_code):
            try:
                error_dict = next(iter((data.items())))
                if "reject_data" in error_dict and isinstance(error_dict[1], dict):
                    index_of = next(iter(error_dict[1]))
                    errors = "".join(
                        error_dict[1]
                        .get(index_of)
                        .get(next(iter(error_dict[1].get(index_of))))[0]
                    )
                    if errors.find("This field is required.") != -1:
                        errors = f"{next(iter(error_dict[1].get(index_of)))} field required in mcq_question at {index_of}."
                    else:
                        errors = (
                            errors.replace(".", "") + f" in mcq_question at {index_of}."
                        )
                else:
                    error_dict = next(iter((data.items())))
                    errors = "".join(iter(error_dict[1]))

                    if errors.find("This field is required.") != -1:
                        errors = f'{error_dict[0]}{errors.replace("This", "")}'
            except:
                errors = data[0]

            response = {"errors": errors}
        return super(DynamicRejectedQuestionRenderer, self).render(
            response, accepted_media_type, renderer_context
        )
