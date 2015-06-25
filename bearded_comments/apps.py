from django.apps import AppConfig


class TCommentConfig(AppConfig):
    name = 'bearded_comments'
    verbose_name = 'Bearded Comments'

    def ready(self):
        import bearded_comments.signals
