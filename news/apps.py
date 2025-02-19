from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals #pylint: disable=unused-argument,missing-final-newline,unused-import,import-outside-toplevel