from django import template
from django.utils.unittest import TestCase

from mock import Mock
from mock import NonCallableMock
from mock import patch

from ..templatetags.o2o_tagging import TaggedInObjects


class TaggedInObjectTest(TestCase):

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

        node = TaggedInObjects.tag(parser, token)

        self.assertTrue(token.contents.split.called)
        search.assert_called_with(r'(.*?) as (\w+)', 'tagged_in as tags')
        self.assertTrue(m.groups.called)
        self.assertEqual(node.tagged_in, Variable.return_value)
        self.assertEqual(node.tags, Variable.return_value)

    @patch('o2o_tagging.templatetags.o2o_tagging.O2OTag', **{'objects.return_value': Mock()})
    def test_render(self, O2OTag):
        tagged_in = NonCallableMock()
        node = TaggedInObjects('tagged_in', 'tags')
        context = self.ContextMock({
            'tagged_in': tagged_in,
        })
        result = node.render(context)

        O2OTag.objects.for_tagged_in.assert_called_with(tagged_in)

        self.assertTrue('tags' in context)
        self.assertEqual(context['tags'],
                         O2OTag.objects.for_tagged_in.return_value)
        self.assertEqual('', result)

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

    def test_tag_register(self):
        from ..templatetags import o2o_tagging

        self.assertTrue(hasattr(o2o_tagging, 'register'))
        self.assertTrue('for_tagged_in' in o2o_tagging.register.tags)
        self.assertTrue(o2o_tagging.register.tags['for_tagged_in'] == TaggedInObjects.tag)
