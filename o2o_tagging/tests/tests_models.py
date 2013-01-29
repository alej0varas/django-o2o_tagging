from django.contrib.contenttypes.generic import GenericForeignKey
from django.test import TestCase
from django.db import IntegrityError

from mock import call
from mock_django.signals import mock_signal_receiver

from ..models import O2OTag
from ..signals import o2o_tag_created

from .models import Tagged
from .models import TaggedIn
from .models import Tagger


class O2OTagTest(TestCase):
    def setUp(self):
        self.tagger = Tagger.objects.create()
        self.tagged = Tagged.objects.create()
        self.tagged_in = TaggedIn.objects.create()

    def test_model_relations_are_GenericForeignKey(self):
        """Test O2OTag contain tagger_content_object,
        tagged_content_object and tagged_in_content_object

        """
        self.assertIsInstance(O2OTag.tagger_content_object, GenericForeignKey)
        self.assertIsInstance(O2OTag.tagged_content_object, GenericForeignKey)
        self.assertIsInstance(O2OTag.tagged_in_content_object,
                              GenericForeignKey)

    def test_model_relations(self):
        """Test creation of `O2OTag` with two generic relations"""
        tag = O2OTag.objects.create(tagger_content_object=self.tagger,
                                    tagged_content_object=self.tagged,
                                    tagged_in_content_object=self.tagged_in)

        self.assertEqual(self.tagger, tag.tagger_content_object)
        self.assertEqual(self.tagged, tag.tagged_content_object)

    def test_model_relations_convenient_properties(self):
        """Test convenient shortcuts `tagger` and `tagged`"""
        tag = O2OTag.objects.create(tagger_content_object=self.tagger,
                                    tagged_content_object=self.tagged,
                                    tagged_in_content_object=self.tagged_in)

        self.assertEqual(self.tagger, tag.tagger)
        self.assertEqual(self.tagged, tag.tagged)
        self.assertEqual(self.tagged_in, tag.tagged_in)

    def test_unique_together(self):
        """Test `tagger`, `tagged` and `tagged_in` are unique together"""
        O2OTag.objects.tag(self.tagger, self.tagged, self.tagged_in)

        self.assertRaises(IntegrityError, O2OTag.objects.tag,
                          self.tagger, self.tagged, self.tagged_in)


class O2OTagManagerTest(TestCase):
    def setUp(self):
        self.tagger = Tagger.objects.create()
        self.tagged = Tagged.objects.create()
        self.tagged_in = TaggedIn.objects.create()
        self.tagger1 = Tagger.objects.create()
        self.tagged1 = Tagged.objects.create()

    def test_tag(self):
        """Test tag method"""
        tag = O2OTag.objects.tag(self.tagger, self.tagged, self.tagged_in)

        self.assertEqual(self.tagger, tag.tagger_content_object)
        self.assertEqual(self.tagged, tag.tagged_content_object)
        self.assertEqual(self.tagged_in, tag.tagged_in_content_object)

    def test_for_tagged_in(self):
        """Test for_tagged_in method. Get all tags where `MyModel` has
        been used as `tagged_in`.

        """
        tag = O2OTag.objects.tag(self.tagger, self.tagged, self.tagged_in)
        tag1 = O2OTag.objects.tag(self.tagger1, self.tagged, self.tagged_in)

        tags = O2OTag.objects.for_tagged_in(self.tagged_in)

        self.assertListEqual([tag, tag1], list(tags))

    def test_for_tagger(self):
        """Test for_tagger method. Get all tags where `MyModel` has
        been used as `tagger`.

        """
        O2OTag.objects.tag(self.tagger, self.tagged, self.tagged_in)
        tag1 = O2OTag.objects.tag(self.tagger1, self.tagged, self.tagged_in)

        tags = O2OTag.objects.for_tagger(self.tagger1)

        self.assertListEqual([tag1], list(tags))

    def test_for_tagged(self):
        """Test for_tagged method. Get all tags where `MyModel` has
        been used as `tagged`.

        """
        tag = O2OTag.objects.tag(self.tagger, self.tagged, self.tagged_in)
        O2OTag.objects.tag(self.tagger, self.tagged1, self.tagged_in)

        tags = O2OTag.objects.for_tagged(self.tagged)

        self.assertListEqual([tag], list(tags))

    def test_for_tagged_in__and__for_tagged_in(self):
        """Test chaining manager methods"""
        tagged_in1 = TaggedIn.objects.create()
        tag = O2OTag.objects.tag(self.tagger, self.tagged, self.tagged_in)
        O2OTag.objects.tag(self.tagger, self.tagged, tagged_in1)
        O2OTag.objects.tag(self.tagger, self.tagged1, tagged_in1)
        O2OTag.objects.tag(self.tagger1, self.tagged, self.tagged_in)
        O2OTag.objects.tag(self.tagger1, self.tagged, tagged_in1)
        O2OTag.objects.tag(self.tagger1, self.tagged1, tagged_in1)

        tags = O2OTag.objects.for_tagged_in(self.tagged_in)
        tags = tags.for_tagger(self.tagger)
        tags = tags.for_tagged(self.tagged)

        self.assertListEqual([tag], list(tags))

    def test_tag_created_signal(self):
        """Test that O2OTag create view send o2o_tag_created signal"""
        with mock_signal_receiver(o2o_tag_created) as tag_created_receiver:
            tag = O2OTag.objects.tag(self.tagger, self.tagged, self.tagged_in)
            self.assertEqual(tag_created_receiver.call_args_list, [
                call(signal=o2o_tag_created, sender=O2OTag, instance=tag),
            ])
