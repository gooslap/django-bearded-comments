from django.test import TestCase
from django.template import Context, Template
from django.contrib.sites.models import Site

from bearded_comments.models import TCommentNode
from bearded_comments.tests import utils


class BeardedCommentsTemplateTagsTest(TestCase):

    def test_render_comment_tree(self):
        from pprint import pprint as pp
        t = Template('{% load comments bearded_comments %}'
                     '{% render_comment_tree for site %}')
        s = Site.objects.get_current()
        c = Context({'site': s})
        utils.create_tcomment_tree(s)
        print(t.render(c))
        pp(TCommentNode.get_annotated_list())
        pp(TCommentNode.dump_bulk())
        #TODO: add real assertions instead of manual output checks 
