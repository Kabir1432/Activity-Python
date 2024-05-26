from django.apps import AppConfig


class ResubmitTaskConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = 'resubmit_task'
    name = __name__.rpartition(".")[0]
