import re

from django import template

from ..models import O2OTag

register = template.Library()


class TaggedInObjects(template.Node):
    def __init__(self, tagged_in, tags):
        self.tagged_in = template.Variable(tagged_in)
        self.tags = template.Variable(tags)

    @classmethod
    def tag(cls, parser, token):
        try:
            tag_name, arg = token.contents.split(None, 1)
        except ValueError:
            raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
        m = re.search(r'(.*?) as (\w+)', arg)
        if not m:
            raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
        tagged_in, tags = m.groups()
        return cls(tagged_in, tags)

    def render(self, context):
        tagged_in = self.tagged_in.resolve(context)
        tags = O2OTag.objects.for_tagged_in(tagged_in)
        context['tags'] = tags
        return ''


register.tag('for_tagged_in', TaggedInObjects.tag)
