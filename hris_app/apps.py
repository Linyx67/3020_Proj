from django.apps import AppConfig


class HrisAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hris_app'

    def ready(self):
        from jobs import updater
        updater.start()
