"""
    Hyperlist app. apps.py for Django framework.
"""
from django.apps import AppConfig


class HyperlistConfig(AppConfig):
    """
        Hyperlist app class
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "hyperlist"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from scheduler import scheduler
        # pylint: enable=import-outside-toplevel
        scheduler.start()
