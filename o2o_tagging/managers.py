from django.db import models


class O2OTagManager(models.Manager):
    def tag(self, tagger, tagged):
        """Create and return a `Tag` from `tagger` to `tagged`"""
        tag = self.create(tagger_content_object=tagger,
                          tagged_content_object=tagged)
        return tag
