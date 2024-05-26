from django.apps import AppConfig


class DashboardcountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = 'dashboardcount'
    name = __name__.rpartition(".")[0]
