import random
import string
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from bearded_comments.models import TComment, TCommentNode
from bearded_comments.forms import TCommentForm

_GTLDS = ['.com', '.net', '.org']

def random_string(len_=5):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len_))

def random_email():
    return ''.join([random_string(), '@', random_string(), random.choice(_GTLDS)])

def random_url():
    return ''.join([random_string(), random.choice(_GTLDS)])

def create_tcomment(target=None, **kwargs):
    """
    Factory for creating TComment instances.
    :param target: Target model of the comment. Defaults to the current Site.
    :return: A new TComment instance.
    """
    site = Site.objects.get_current()
    target_ = target if target else site
    # content_type, object_pk, timestamp, security_hash
    security_data = TCommentForm(target_).generate_security_data()
    # Base django_comments data
    data = {
        'content_type': ContentType.objects.get_for_model(target_),
        'object_pk': security_data['object_pk'],
        'user_name': random_string(),
        'user_email': random_email(),
        'user_url': random_url(),
        'comment': random_string(25),
        'submit_date': timezone.now(),
        'site_id': site.pk,
        'is_public': True,
        'is_removed': False
    }
    # Extended TComment data
    data.update({
        'title': random_string()
    })
    # Caller override auto-generated fields
    data.update(kwargs)
    return TComment(**data)

def create_tcomment_node(comment=None, parent=None):
    """
    Factory for creating TCommentNode instances.
    """
    pass

def create_tcomment_tree(target=None, 
                         max_depth=3, 
                         max_children=3, 
                         with_signal=False,
                         depth=1, 
                         parent=None):
    """
    Recursively populate the database with a random tree of depth max_depth.
    """
    if depth <= max_depth:
        children = random.randrange(1, max_children + 1)
        for _ in range(children):
            c = create_tcomment(target)
            c.save()
            if parent:
                node = parent.node.add_child(comment=c)
            else:
                node = TCommentNode.add_root(comment=c)
            c.node = node
            c.save()
            create_tcomment_tree(target, depth=depth+1, parent=c, with_signal=with_signal)





