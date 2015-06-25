from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django_comments.models import Comment as CommentBase
from treebeard.mp_tree import MP_Node


class TComment(CommentBase):
    """
    Extension of django-contrib-comments Comment for use in tree structure.
    """
    title = models.TextField(_('Title'), blank=True)

    def __str__(self):
        return 'Comment (threaded): %s' % super().__str__()

    class Meta(object):
        verbose_name = _('Comment (threaded)')
        verbose_name_plural = _('Comments (threaded)')

class TCommentNode(MP_Node):
    """
    Materialized Path node to store comments in a tree structure.

    These are generally created when the comment_was_posted signal
    is sent by the django_comments post_comment view. Similarly,
    they are rendered using the template tags [...].
    """
    comment = models.OneToOneField(TComment, related_name='node')
    insertion_date = models.DateTimeField(_('date/time inserted'), default=now)

    # Maybe want to store date in the same table for performance reasons.
    node_order_by = ['insertion_date']

    def __str__(self):
        return super().__str__()

