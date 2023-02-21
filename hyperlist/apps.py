from django.apps import AppConfig


class HyperlistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hyperlist"

    def ready(self):
        from scheduler import scheduler
        scheduler.start()
