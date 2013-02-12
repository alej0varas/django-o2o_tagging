import re

from django import template

from ..models import O2OTag

register = template.Library()


class BaseTaggedInObjects(template.Node):
    distinct = False

    def __init__(self, tagged_in, tags):
        self.tagged_in = template.Variable(tagged_in)
        self.tags = template.Variable(tags)

    @classmethod
    def tag(cls, parser, token):
        try:
            tag_name, arg = token.contents.split(None, 1)
        except ValueError:
            raise template.TemplateSyntaxError(
                "%r tag requires arguments" % token.contents.split()[0])
        m = re.search(r'(.*?) as (\w+)', arg)
        if not m:
            raise template.TemplateSyntaxError(
                "%r tag had invalid arguments" % tag_name)
        tagged_in, tags = m.groups()
        return cls(tagged_in, tags)

    def render(self, context):
        tagged_in = self.tagged_in.resolve(context)
        tags = O2OTag.objects.all()
        tags = self.filter(tags, tagged_in)
        context['tags'] = tags
        return ''

    def filter(self, tags, tagged_in):
        raise NotImplementedError('Method must be implemented in child class')


class TaggedInObjects(BaseTaggedInObjects):

    def filter(self, tags, tagged_in):
        tags = tags.for_tagged_in(tagged_in)
        return tags


class TaggedInObjectsNoDups(BaseTaggedInObjects):

    def filter(self, tags, tagged_in):
        tags = tags.for_tagged_in_nodups(tagged_in)
        return tags


register.tag('for_tagged_in', TaggedInObjects.tag)
register.tag('for_tagged_in_nodups', TaggedInObjectsNoDups.tag)
