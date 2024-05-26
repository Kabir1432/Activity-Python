from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = 'student'
    name = __name__.rpartition(".")[0]

    def ready(self):
        import activityngo.student.signals
