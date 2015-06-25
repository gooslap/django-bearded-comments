from unittest.mock import MagicMock
from django.test import TestCase
from django.http import HttpRequest, QueryDict
from django_comments.signals import comment_was_flagged, \
                                    comment_was_posted, \
                                    comment_will_be_posted

from bearded_comments.models import TCommentNode
from bearded_comments.tests.utils import create_tcomment


class CommentWasPostedTest(TestCase):

    def setUp(self):
        self.request = MagicMock(
            spec=HttpRequest,
            POST=MagicMock(spec=QueryDict))

    def _assert_responses_true(self, responses):
        for (receiver, response) in responses:
            self.assertTrue(
                response,
                msg='receiver: %s, response: %s' % (receiver, response))

    def test_noparent_rootnode_wasadded(self):
        comment = create_tcomment()
        comment.save()
        self.request.POST = {'parent': ''}
        responses = comment_was_posted.send(
            sender=comment.__class__,
            comment=comment,
            request=self.request)

        self._assert_responses_true(responses)
        self.assertTrue(comment.node.is_root())

    def test_parent_childnode_wasadded(self):
        parent_comment = create_tcomment()
        parent_comment.save()
        parent_node = TCommentNode.add_root(comment=parent_comment)
        comment = create_tcomment()
        comment.save()
        self.request.POST = {'parent': parent_node.pk}
        responses = comment_was_posted.send(
            sender=comment.__class__,
            comment=comment,
            request=self.request)

        self._assert_responses_true(responses)
        self.assertEqual(parent_node, comment.node.get_parent())
