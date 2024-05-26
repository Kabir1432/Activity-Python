from django.apps import AppConfig


class FcmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = 'fcm'
    name = __name__.rpartition(".")[0]
