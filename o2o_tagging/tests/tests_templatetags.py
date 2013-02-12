from django import template
from django.utils.unittest import TestCase

from mock import Mock
from mock import patch

from ..templatetags.o2o_tagging import BaseTaggedInObjects
from ..templatetags.o2o_tagging import TaggedInObjects
from ..templatetags.o2o_tagging import TaggedInObjectsNoDups


class BaseTaggedInObjectTest(TestCase):

    tag_name = 'for_tagged_in'

    class ContextMock(dict):
        autoescape = object()

    O2OTagMock = Mock()

    @patch('re.search')
    @patch('django.template.Variable')
    def test_tag(self, Variable, search):
        parser = Mock()
        token = Mock()
        token.contents = Mock(methods=['split'])
        token.contents.split.return_value = ['tagged_in_object',
                                             'tagged_in as tags']
        m = Mock()
        m.groups.return_value = ('tagged_in', 'tags')
        search.return_value = m

        node = BaseTaggedInObjects.tag(parser, token)

        self.assertTrue(token.contents.split.called)
        search.assert_called_with(r'(.*?) as (\w+)', 'tagged_in as tags')
        self.assertTrue(m.groups.called)
        self.assertEqual(node.tagged_in, Variable.return_value)
        self.assertEqual(node.tags, Variable.return_value)

    @patch('o2o_tagging.templatetags.o2o_tagging.O2OTag', **{'objects.return_value': Mock()})
    def test_filter(self, O2OTag):
        tags = None
        tagged_in = None
        node = BaseTaggedInObjects('tagged_in', 'tags')

        self.assertRaises(NotImplementedError, node.filter, tags, tagged_in)

    def test_tag_insuficient_arguments(self):
        parser = Mock()
        token = Mock()
        token.contents = Mock(methods=['split'])
        token.contents.split.return_value = ['tagged_in_object',
                                             'tagged_in as']

        self.assertRaises(template.TemplateSyntaxError,
                          TaggedInObjects.tag, parser, token)

    def test_tag_bad_arguments(self):
        parser = Mock()
        token = Mock()
        token.contents = Mock(methods=['split'])
        token.contents.split.return_value = ['tagged_in_object',
                                             'tagged_in asdf tags']

        self.assertRaises(template.TemplateSyntaxError,
                          TaggedInObjects.tag, parser, token)

    def test_tag_no_arguments(self):
        parser = Mock()
        token = Mock()
        token.contents = Mock(methods=['split'])
        token.contents.split.return_value = ['tagged_in_object', ]

        self.assertRaises(template.TemplateSyntaxError,
                          TaggedInObjects.tag, parser, token)


class TaggedInObjectsTest(BaseTaggedInObjectTest):

    tag_name = 'for_tagged_in'

    def test_render(self):
        obj = TaggedInObjects('tagged_in', 'tags')
        tags = Mock()
        tagged_in = Mock()

        obj.filter(tags, tagged_in)

        self.assertTrue(tags.for_tagged_in.called)

    def test_tag_register(self):
        from ..templatetags import o2o_tagging

        self.assertTrue(hasattr(o2o_tagging, 'register'))
        self.assertTrue(self.tag_name in o2o_tagging.register.tags)
        self.assertEqual(o2o_tagging.register.tags[self.tag_name],
                         TaggedInObjects.tag)


class TaggedInObjectsNoDupsTest(BaseTaggedInObjectTest):

    tag_name = 'for_tagged_in_nodups'

    def test_render(self):
        obj = TaggedInObjectsNoDups('tagged_in', 'tags')
        tags = Mock()
        tagged_in = Mock()

        obj.filter(tags, tagged_in)

        self.assertTrue(tags.for_tagged_in_nodups.called)

    def test_tag_register(self):
        from ..templatetags import o2o_tagging

        self.assertTrue(hasattr(o2o_tagging, 'register'))
        self.assertTrue(self.tag_name in o2o_tagging.register.tags)
        self.assertEqual(o2o_tagging.register.tags[self.tag_name],
                         TaggedInObjectsNoDups.tag)
