=============
 o2o_tagging
=============

|build status|_

.. |build status| image:: https://api.travis-ci.org/alej0varas/django-o2o_tagging.png?branch=master
   :alt: Build Status
.. _build status: https://travis-ci.org/alej0varas/django-o2o_tagging

Welcome to the documentation for django-o2o_tagging! Use this app to
tag objects like you tag your friends on facebook, but using any
objects as the tagger, the tagged and the tagged in. Think of a `User`
tagging a `Friend` in a `Photo` all of them being different models.

Quick start
-----------

1. Install using pip::

    pip install django-o2o_tagging

#. Add o2o_tagging to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'o2o_tagging',
      )

Usage
-----

1. Models

    Tag your objects::

        ...
        tag = O2OTag.objects.tag(tagger, tagged, tagged_in)


    Get for tagged in objects::

        ...
        tags = O2OTag.objects.for_tagged_in(tagged_in)

    Get for tagger objects::

        ...
        tags = O2OTag.objects.for_tagger(tagger)

    Get for tagged objects::

        ...
        tags = O2OTag.objects.for_tagged(tagged)

    You can then filter::

        ...
        tags.for_tagger(tagger).for_tagged(tagged)

#. URLs

    You can add this views to your urls::

        ...
        ('^tagging/$', include('o2o_tagging')),

#. Views

    o2o_taggin provides two views::

        TagCreateView

        TagsCreateView

Running the Tests
-----------------

You can run the tests with via::

    python setup.py test
