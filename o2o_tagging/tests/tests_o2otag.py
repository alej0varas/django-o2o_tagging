from django.contrib.contenttypes.generic import GenericForeignKey
from django.test import TestCase

from ..models import O2OTag

from .models import Tagged
from .models import TaggedIn
from .models import Tagger


class O2OTagTest(TestCase):
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
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()
        tagged_in = TaggedIn.objects.create()

        tag = O2OTag.objects.create(tagger_content_object=tagger,
                                    tagged_content_object=tagged,
                                    tagged_in_content_object=tagged_in)

        self.assertEqual(tagger, tag.tagger_content_object)
        self.assertEqual(tagged, tag.tagged_content_object)

    def test_model_relations_convenient_properties(self):
        """Test convenient shortcuts `tagger` and `tagged`"""
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()
        tagged_in = TaggedIn.objects.create()

        tag = O2OTag.objects.create(tagger_content_object=tagger,
                                    tagged_content_object=tagged,
                                    tagged_in_content_object=tagged_in)

        self.assertEqual(tagger, tag.tagger)
        self.assertEqual(tagged, tag.tagged)
        self.assertEqual(tagged_in, tag.tagged_in)


class O2OTagManagerTest(TestCase):
    def test_tag(self):
        """Test tag method"""
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()
        tagged_in = TaggedIn.objects.create()

        tag = O2OTag.objects.tag(tagger, tagged, tagged_in)

        self.assertEqual(tagger, tag.tagger_content_object)
        self.assertEqual(tagged, tag.tagged_content_object)
        self.assertEqual(tagged_in, tag.tagged_in_content_object)

    def test_for_tagged_in(self):
        """Test for_tagged_in method. Get all tags where `MyModel` has
        been used as `tagged_in`.

        """
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()
        tagged_in = TaggedIn.objects.create()
        tag = O2OTag.objects.tag(tagger, tagged, tagged_in)
        tag1 = O2OTag.objects.tag(tagger, tagged, tagged_in)

        tags = O2OTag.objects.for_tagged_in(tagged_in)

        self.assertListEqual([tag, tag1], list(tags))

    def test_for_tagger(self):
        """Test for_tagger method. Get all tags where `MyModel` has
        been used as `tagger`.

        """
        tagger = Tagger.objects.create()
        tagger1 = Tagger.objects.create()
        tagged = Tagged.objects.create()
        tagged_in = TaggedIn.objects.create()
        O2OTag.objects.tag(tagger, tagged, tagged_in)
        tag1 = O2OTag.objects.tag(tagger1, tagged, tagged_in)

        tags = O2OTag.objects.for_tagger(tagger1)

        self.assertListEqual([tag1], list(tags))

    def test_for_tagged(self):
        """Test for_tagged method. Get all tags where `MyModel` has
        been used as `tagged`.

        """
        tagger = Tagger.objects.create()
        tagged = Tagged.objects.create()
        tagged1 = Tagged.objects.create()
        tagged_in = TaggedIn.objects.create()
        tag = O2OTag.objects.tag(tagger, tagged, tagged_in)
        O2OTag.objects.tag(tagger, tagged1, tagged_in)

        tags = O2OTag.objects.for_tagged(tagged)

        self.assertListEqual([tag], list(tags))

    def test_for_tagged_in__and__for_tagged_in(self):
        """Test chaining manager methods"""
        tagger = Tagger.objects.create()
        tagger1 = Tagger.objects.create()
        tagged = Tagged.objects.create()
        tagged1 = Tagged.objects.create()
        tagged_in = TaggedIn.objects.create()
        tagged_in1 = TaggedIn.objects.create()
        tag = O2OTag.objects.tag(tagger, tagged, tagged_in)
        O2OTag.objects.tag(tagger, tagged, tagged_in1)
        O2OTag.objects.tag(tagger, tagged1, tagged_in1)
        O2OTag.objects.tag(tagger1, tagged, tagged_in)
        O2OTag.objects.tag(tagger1, tagged, tagged_in1)
        O2OTag.objects.tag(tagger1, tagged1, tagged_in1)

        tags = O2OTag.objects.for_tagged_in(tagged_in).for_tagger(
            tagger).for_tagged(tagged)

        self.assertListEqual([tag], list(tags))
