from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_comments.forms import CommentForm as CommentFormBase

from bearded_comments.models import TComment
from bearded_comments.models import TCommentNode
from bearded_comments import settings

class TCommentForm(CommentFormBase):
    title = forms.CharField(label=_('Title'), required=False, max_length=settings.COMMENTS_TITLE_MAX_LENGTH)
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent: # For non-root comments
            try:
                TCommentNode.objects.get(pk=parent)
            except TCommentNode.DoesNotExist:
                raise ValidationError(_('Parent comment node %s does not exist') % parent, code='invalid')
        return parent

    def get_comment_model(self):
        return TComment

    def get_comment_create_data(self):
        """
        Extends base method adding 'title' data to the result.
        """
        data = super().get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        return data