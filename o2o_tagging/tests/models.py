from django.db import models


class Tagged(models.Model):
    def __unicode__(self):
        return u'%s' % self.pk


class Tagger(models.Model):
    def __unicode__(self):
        return u'%s' % self.pk


class TaggedIn(models.Model):
    def __unicode__(self):
        return u'%s' % self.pk
