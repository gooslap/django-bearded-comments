from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.contrib.sites.models import Site
from bearded_comments.models import TComment, TCommentNode
from bearded_comments.forms import TCommentForm

class TCommentFormTest(TestCase):

    def setUp(self):
        # Establish mock target for the comments
        self.site = Site.objects.get_current()
        # Create a mock content_type, object_pk, timestamp, security_hash
        self.security_data = TCommentForm(self.site).generate_security_data()

    def _get_test_comment_data(self):
        return {
            'title': 'Powerpuff',
            'name': 'Buttercup',
            'email': 'bcup@example.com',
            'url': 'bcup.example.com',
            'comment': "Cheer up, buttercup. You're going to make some cats very happy one day."
        }

    def test_clean_noparent_success(self):
        data = self._get_test_comment_data()
        data.update(self.security_data)
        form = TCommentForm(self.site, data=data)
        self.assertTrue(form.is_valid(), msg='form.errors: %s' % form.errors.as_data())

    def test_clean_parent_invalid_parent_fail(self):
        data = self._get_test_comment_data()
        data.update(self.security_data)
        data.update({'parent': '2'})
        form = TCommentForm(self.site, data=data)
        self.assertFalse(form.is_valid(), msg='form.errors: %s' % form.errors.as_data())

    def test_clean_parent_valid_parent_success(self):
        another_site = Site.objects.create(domain='duckduckgo.com', name='duckduckgo')
        comment = TComment.objects.create(
            user_name='Bubbles',
            user_email='bubs@example.com',
            comment='Sugar and spice',
            content_type=ContentType.objects.get_for_model(Site),
            site=self.site,
            object_pk=another_site.pk
        )
        node = TCommentNode.add_root(comment=comment)
        data = self._get_test_comment_data()
        data.update(self.security_data)
        data.update({'parent': str(node.pk)})
        form = TCommentForm(another_site, data=data)
        self.assertTrue(form.is_valid(), msg='form.errors: %s' % form.errors.as_data())

