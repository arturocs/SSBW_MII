from django.apps import AppConfig


class SenderosAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'senderos_app'
    def ready(self):
        import senderos_app.signals