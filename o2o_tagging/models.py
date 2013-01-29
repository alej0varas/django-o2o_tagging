from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from model_utils.managers import PassThroughManager

from .managers import O2OTagQuerySet


class O2OTag(models.Model):
    # The object that is tagging
    tagger_content_type = models.ForeignKey(ContentType,
                                            related_name="taggers")
    tagger_object_id = models.PositiveIntegerField()
    tagger_content_object = generic.GenericForeignKey("tagger_content_type",
                                                      "tagger_object_id")

    # The object that is tagged
    tagged_content_type = models.ForeignKey(ContentType,
                                            related_name="taggeds")
    tagged_object_id = models.PositiveIntegerField()
    tagged_content_object = generic.GenericForeignKey("tagged_content_type",
                                                      "tagged_object_id")

    # The object where the tagged objects is tagged
    tagged_in_content_type = models.ForeignKey(
        ContentType,
        related_name="tags")
    tagged_in_object_id = models.PositiveIntegerField()
    tagged_in_content_object = generic.GenericForeignKey(
        "tagged_in_content_type",
        "tagged_in_object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    objects = PassThroughManager.for_queryset_class(O2OTagQuerySet)()

    class Meta:
        unique_together = ('tagger_content_type', 'tagger_object_id',
                           'tagged_content_type', 'tagged_object_id',
                           'tagged_in_content_type', 'tagged_in_object_id')

    def __unicode__(self):
        return u'%s -> %s | %s' % (self.tagger, self.tagged, self.tagged_in)

    # Convenient shortcuts
    @property
    def tagged(self):
        return self.tagged_content_object

    @property
    def tagger(self):
        return self.tagger_content_object

    @property
    def tagged_in(self):
        return self.tagged_in_content_object
