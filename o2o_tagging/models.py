from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


from .managers import O2OTagManager


class O2OTag(models.Model):
    tagger_content_type = models.ForeignKey(ContentType,
                                            related_name="taggers")
    tagger_object_id = models.PositiveIntegerField()
    tagger_content_object = generic.GenericForeignKey("tagger_content_type",
                                                      "tagger_object_id")

    tagged_content_type = models.ForeignKey(ContentType,
                                            related_name="taggeds")
    tagged_object_id = models.PositiveIntegerField()
    tagged_content_object = generic.GenericForeignKey("tagged_content_type",
                                                      "tagged_object_id")

    objects = O2OTagManager()

    tagged = tagged_content_object  # Convenient shortcuts
    tagger = tagger_content_object  # Convenient shortcuts
