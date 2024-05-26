from django.apps import AppConfig


class SubAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = __name__.rpartition(".")[0]

    def ready(self):
        import activityngo.sub_admin.signals
