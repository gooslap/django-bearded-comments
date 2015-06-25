from django.contrib import admin
from bearded_comments.models import TCommentNode
from bearded_comments.models import TComment
from django_comments.admin import CommentsAdmin as BaseCommentsAdmin


class TCommentNodeInline(admin.StackedInline):
    model = TCommentNode


@admin.register(TComment)
class TCommentAdmin(BaseCommentsAdmin):
    """
    Extends comments admin to link with comment node in tree.
    """
    inlines = [TCommentNodeInline]

