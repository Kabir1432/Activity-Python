from django.apps import AppConfig


class TaskEvaluationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = 'task_evaluation'
    name = __name__.rpartition(".")[0]
