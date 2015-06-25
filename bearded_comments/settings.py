from django.conf import settings

COMMENTS_TITLE_MAX_LENGTH = getattr(settings, 'BEARDED_COMMENTS_TITLE_MAX_LENGTH', 255)
