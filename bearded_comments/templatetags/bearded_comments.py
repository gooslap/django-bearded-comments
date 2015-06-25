from django_comments.templatetags.comments import BaseCommentNode
from django.template.loader import render_to_string
from django import template
from django.conf import settings
from django.utils.encoding import smart_text

import bearded_comments

register = template.Library()


class CommentTreeNode(BaseCommentNode):
    """Insert a tree of comment Nodes into the context."""

    def __init__(self, *args, **kwargs):
        """
        Extends base method adding the proper treebeard Node.
        """
        super().__init__(*args, **kwargs)
        self.comment_node = bearded_comments.get_node()

    def get_queryset(self, context):
        """
        Overrides base method to return a collection of comment root nodes.
        """
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.comment_model.objects.none()

        qs = self.comment_node.objects.filter(
            depth=1,
            comment__content_type=ctype,
            comment__object_pk=smart_text(object_pk),
            comment__site__pk=settings.SITE_ID)

        # Only filter on is_public and is_removed fields if they exist.
        field_names = [f.name for f in self.comment_model._meta.fields]
        if 'is_public' in field_names:
            qs = qs.filter(comment__is_public=True)
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            qs = qs.filter(comment__is_removed=False)

        return qs

    def get_context_value_from_queryset(self, context, qs):
        """
        Overrides base method to return an annotated list of comment nodes for each.

        See the treebeard docs 'https://tabo.pe/projects/django-treebeard/docs/2.0/api.html'
        for notes on how to iterate through the annotated list.
        """
        result = list()
        for node in qs:
            result.extend(self.comment_node.get_annotated_list(node))
        return result


class RenderCommentTreeNode(CommentTreeNode):
    """Render the comment tree directly"""

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_tree and return a Node."""
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% render_comment_tree for obj %}
        if len(tokens) == 3:
            return cls(object_expr=parser.compile_filter(tokens[2]))

        # {% render_comment_tree for app.models pk %}
        elif len(tokens) == 4:
            return cls(
                ctype=super().lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr=parser.compile_filter(tokens[3])            )

    def render(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            template_search_list = [
                "comments/%s/%s/tree.html" % (ctype.app_label, ctype.model),
                "comments/%s/tree.html" % ctype.app_label,
                "comments/tree.html"
            ]
            qs = self.get_queryset(context)
            context.push()
            treestr = render_to_string(template_search_list, {
                "comment_tree": self.get_context_value_from_queryset(context, qs)
            }, context)
            context.pop()
            return treestr
        else:
            return ''


@register.tag
def get_comment_tree(parser, token):
    """
    Gets the tree of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_comment_tree for [object] as [varname]  %}
        {% get_comment_tree for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_comment_tree for event as comment_tree %}
        {% for comment in comment_list %}
            ...
        {% endfor %}

    """
    return CommentTreeNode.handle_token(parser, token)


@register.tag
def render_comment_tree(parser, token):
    """
    Render the comment tree (as returned by ``{% get_comment_tree %}``)
    through the ``comments/tree.html`` template

    Syntax::

        {% render_comment_tree for [object] %}
        {% render_comment_tree for [app].[model] [object_id] %}

    Example usage::

        {% render_comment_tree for event %}

    """
    return RenderCommentTreeNode.handle_token(parser, token)