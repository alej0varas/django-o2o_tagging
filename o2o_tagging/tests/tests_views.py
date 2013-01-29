from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from ..models import O2OTag

from .models import Tagged
from .models import TaggedIn
from .models import Tagger


class TagCreateViewTest(TestCase):
    def setUp(self):
        self.tagger = Tagger.objects.create()
        self.tagger_content_type = ContentType.objects.get_for_model(Tagger)
        self.tagged = Tagged.objects.create()
        self.tagged_content_type = ContentType.objects.get_for_model(Tagged)
        self.tagged_in = TaggedIn.objects.create()
        self.tagged_in_content_type = ContentType.objects.get_for_model(
            TaggedIn)
        self.data = {'tagger_object_id': self.tagger.pk,
                     'tagger_content_type': self.tagger_content_type.pk,
                     'tagged_object_id': self.tagged.pk,
                     'tagged_content_type': self.tagged_content_type.pk,
                     'tagged_in_object_id': self.tagged_in.pk,
                     'tagged_in_content_type': self.tagged_in_content_type.pk,
                     }
        self.url = reverse('o2o_taggin_tag_create')

    def test_tag_create(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(201, response.status_code)

        tag = O2OTag.objects.get()

        self.assertEqual(self.tagger, tag.tagger)
        self.assertEqual(self.tagged, tag.tagged)
        self.assertEqual(self.tagged_in, tag.tagged_in)

    def test_tag_create__form_errors(self):
        url = reverse('o2o_taggin_tag_create')

        data = {}

        response = self.client.post(url, data)

        self.assertEqual(400, response.status_code)

        count = O2OTag.objects.count()

        self.assertEqual(0, count)
