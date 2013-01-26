from django.contrib.contenttypes.generic import GenericForeignKey
from django.test import TestCase

from ..models import O2OTag

from .models import Tagged
from .models import Tagger


class O2OTagTest(TestCase):
    def test_model_relations_are_GenericForeignKey(self):
        """Test model contain two generic relations"""
        self.assertIsInstance(O2OTag.tagger_content_object, GenericForeignKey)
        self.assertIsInstance(O2OTag.tagged_content_object, GenericForeignKey)

    def test_model_relations(self):
        """Test creation of `O2OTag` with two generic relations"""
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()

        tag = O2OTag.objects.create(tagger_content_object=tagger,
                                    tagged_content_object=tagged)

        self.assertEqual(tagger, tag.tagger_content_object)
        self.assertEqual(tagged, tag.tagged_content_object)

    def test_model_relations_convenient_properties(self):
        """Test convenient shortcuts `tagger` and `tagged`"""
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()

        tag = O2OTag.objects.create(tagger_content_object=tagger,
                                    tagged_content_object=tagged)

        self.assertEqual(tagger, tag.tagger)
        self.assertEqual(tagged, tag.tagged)


class O2OTagManagerTest(TestCase):
    def test_tagger_relation(self):
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()

        tag = O2OTag.objects.tag(tagger, tagged)

        self.assertEqual(tagger, tag.tagger_content_object)
        self.assertEqual(tagged, tag.tagged_content_object)
