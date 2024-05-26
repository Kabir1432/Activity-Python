from django.apps import AppConfig


class DiscountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = 'discount'
    name = __name__.rpartition(".")[0]

    def ready(self):
        import activityngo.discount.signals
