from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.test import TestCase

from mock_django.http import MockHttpRequest

from ..forms import TagFormAuthenticated
from ..forms import TagFormAuthenticatedSet
from ..models import O2OTag

from .models import Tagged
from .models import TaggedIn
from .models import Tagger


class TagsCreateFormTest(TestCase):
    def setUp(self):
        self.tagger = Tagger.objects.create()
        self.tagger_content_type = ContentType.objects.get_for_model(Tagger)
        self.tagged = Tagged.objects.create()
        self.tagged1 = Tagged.objects.create()
        self.tagged_content_type = ContentType.objects.get_for_model(Tagged)
        self.tagged_in = TaggedIn.objects.create()
        self.tagged_in_content_type = ContentType.objects.get_for_model(
            TaggedIn)
        self.data = {
            'form-TOTAL_FORMS': u'2',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-tagged_object_id': self.tagged.pk,
            'form-0-tagged_content_type': self.tagged_content_type.pk,
            'form-0-tagged_in_object_id': self.tagged_in.pk,
            'form-0-tagged_in_content_type': self.tagged_in_content_type.pk,
            'form-1-tagged_object_id': self.tagged1.pk,
            'form-1-tagged_content_type': self.tagged_content_type.pk,
            'form-1-tagged_in_object_id': self.tagged_in.pk,
            'form-1-tagged_in_content_type': self.tagged_in_content_type.pk,
        }

    def test_save__tagger_is_request_user(self):
        tags_form = TagFormAuthenticatedSet(self.data)
        tags_form.clean()
        request = MockHttpRequest(POST=self.data)
        request.user = self.tagger

        tags = tags_form.save(request)
        expected_tags = list(O2OTag.objects.filter())

        self.assertIsInstance(tags, QuerySet)
        self.assertListEqual(expected_tags, list(tags))


class TagCreateFormTest(TestCase):
    def setUp(self):
        self.tagger = Tagger.objects.create()
        self.tagger_content_type = ContentType.objects.get_for_model(Tagger)
        self.tagged = Tagged.objects.create()
        self.tagged1 = Tagged.objects.create()
        self.tagged_content_type = ContentType.objects.get_for_model(Tagged)
        self.tagged_in = TaggedIn.objects.create()
        self.tagged_in_content_type = ContentType.objects.get_for_model(
            TaggedIn)
        self.data = {
            'tagged_object_id': self.tagged.pk,
            'tagged_content_type': self.tagged_content_type.pk,
            'tagged_in_object_id': self.tagged_in.pk,
            'tagged_in_content_type': self.tagged_in_content_type.pk,
        }

    def test_save__tagger_is_request_user(self):
        tag_form = TagFormAuthenticated(self.data)
        tag_form.is_valid()
        request = MockHttpRequest(POST=self.data)
        request.user = self.tagger

        tag = tag_form.save(request=request)
        expected_tag = O2OTag.objects.get()

        self.assertIsInstance(tag, O2OTag)
        self.assertEqual(expected_tag, tag)
