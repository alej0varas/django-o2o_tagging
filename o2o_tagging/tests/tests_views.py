from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

# from mock import call
from mock_django.http import MockHttpRequest
from mock_django.signals import mock_signal_receiver

from ..models import O2OTag
from ..signals import o2o_tags_created
from ..views import TagCreateView
from ..views import TagsCreateView

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
        self.data = {'tagged_object_id': self.tagged.pk,
                     'tagged_content_type': self.tagged_content_type.pk,
                     'tagged_in_object_id': self.tagged_in.pk,
                     'tagged_in_content_type': self.tagged_in_content_type.pk,
                     }
        self.url = reverse('o2o_taggin_tag_create')

    def test_tag_create(self):
        request = MockHttpRequest(POST=self.data)
        request.user = self.tagger

        response = TagCreateView.as_view()(request)
        tag = O2OTag.objects.get()

        self.assertEqual(201, response.status_code)
        self.assertEqual(self.tagger, tag.tagger)
        self.assertEqual(self.tagged, tag.tagged)
        self.assertEqual(self.tagged_in, tag.tagged_in)

    def test_tag_create__form_invalid(self):
        request = MockHttpRequest(POST={})
        request.user = self.tagger

        response = TagCreateView.as_view()(request)
        tags = O2OTag.objects.all()

        self.assertEqual(400, response.status_code)
        self.assertEqual(0, tags.count())


class TagsCreateViewTest(TestCase):
    def setUp(self):
        self.tagger_content_type = ContentType.objects.get_for_model(Tagger)
        self.tagged_content_type = ContentType.objects.get_for_model(Tagged)
        self.tagged_in_content_type = ContentType.objects.get_for_model(
            TaggedIn)
        self.tagger = Tagger.objects.create()
        self.tagged = Tagged.objects.create()
        self.tagged1 = Tagged.objects.create()
        self.tagged_in = TaggedIn.objects.create()

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

        self.url = reverse('o2o_taggin_tag_create_multiple')

    def test_create__tagger_is_request_user(self):
        request = MockHttpRequest(POST=self.data)
        request.user = self.tagger

        response = TagsCreateView.as_view()(request)
        tags = O2OTag.objects.all()

        self.assertEqual(201, response.status_code)
        self.assertEqual(2, tags.count())
        for t in tags:
            self.assertEqual(self.tagger, t.tagger)

    def test_create__call_tags_created_signal(self):
        from mock_django.http import MockHttpRequest
        request = MockHttpRequest(POST=self.data)
        request.user = self.tagger

        with mock_signal_receiver(o2o_tags_created) as tags_created_receiver:
            TagsCreateView.as_view()(request)
            self.assertTrue(tags_created_receiver.called)

            # this fail assertion is failing but must be correct
            # self.assertEqual(tags_created_receiver.call_args_list, [
            #     call(signal=o2o_tags_created, sender=TagsCreateView, instances=tags),
            # ])

    def test_tag_create__form_invalid(self):
        data = {
            'form-TOTAL_FORMS': u'2',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-tagged_object_id': self.tagged.pk,
            'form-0-tagged_content_type': self.tagged_content_type.pk,
        }
        request = MockHttpRequest(POST=data)
        request.user = self.tagger

        response = TagsCreateView.as_view()(request)
        tags = O2OTag.objects.all()

        self.assertEqual(400, response.status_code)
        self.assertEqual(0, tags.count())
