from django.dispatch import receiver
from django_comments.signals import comment_was_flagged, \
                                    comment_was_posted, \
                                    comment_will_be_posted

from bearded_comments.models import TComment, TCommentNode


@receiver(comment_was_posted, sender=TComment)
def add_comment_node(sender, **kwargs):
    comment = kwargs['comment']
    request = kwargs['request']
    parent = request.POST['parent']
    if parent:
        pnode = TCommentNode.objects.get(pk=parent)
        node = pnode.add_child(comment=comment)
    else:
        node = TCommentNode.add_root(comment=comment)

    return True if node else False