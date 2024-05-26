from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = 'project'
    name = __name__.rpartition(".")[0]
