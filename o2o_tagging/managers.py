from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

from .signals import o2o_tag_created


class O2OTagQuerySet(QuerySet):
    def tag(self, tagger, tagged, tagged_in):
        """Create and return a `Tag` from `tagger` to `tagged` in
        `tagged_in`

        """
        tag = self.create(tagger_content_object=tagger,
                          tagged_content_object=tagged,
                          tagged_in_content_object=tagged_in)
        o2o_tag_created.send(self.model, instance=tag)
        return tag

    def for_tagged_in(self, tagged_in):
        """Get all tags that belogns to `tagged_in`"""
        tagged_in_model = tagged_in.__class__
        tagged_in_content_type = ContentType.objects.get_for_model(
            tagged_in_model)
        return self.filter(tagged_in_content_type=tagged_in_content_type,
                           tagged_in_object_id=tagged_in.pk)

    def for_tagger(self, tagger):
        """Get all tags that belogns to `tagger`"""
        tagger_model = tagger.__class__
        tagger_content_type = ContentType.objects.get_for_model(
            tagger_model)
        return self.filter(tagger_content_type=tagger_content_type,
                           tagger_object_id=tagger.pk)

    def for_tagged(self, tagged):
        """Get all tags that tag to `tagged`"""
        tagged_model = tagged.__class__
        tagged_content_type = ContentType.objects.get_for_model(
            tagged_model)
        return self.filter(tagged_content_type=tagged_content_type,
                           tagged_object_id=tagged.pk)
