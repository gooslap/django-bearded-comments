
__version__ = "0.0.0"

def get_node():
    from .models import TCommentNode
    return TCommentNode

def get_model():
    from .models import TComment
    return TComment

def get_form():
    from .forms import TCommentForm
    return TCommentForm


default_app_config = 'bearded_comments.apps.TCommentConfig'
