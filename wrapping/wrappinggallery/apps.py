from django.apps import AppConfig


class WrappinggalleryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wrappinggallery"

    def ready(self):
        pass  # Ensure this is imported
