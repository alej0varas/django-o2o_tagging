=============
 o2o_tagging
=============

|build status|_

.. |build status| image:: https://api.travis-ci.org/alej0varas/django-o2o_tagging.png?branch=master
   :alt: Build Status
.. _build status: https://travis-ci.org/alej0varas/django-o2o_tagging

Welcome to the documentation for django-o2o_tagging! Use this app to
tag objects like you tag your friends on facebook, but using any
objects as the tagger and the tagged.

Quick start
-----------

1. Install using pip::

    pip install django-o2o_tagging

2. Create your models and inherit from o2o_tagging.O2OTag::

    ...
    class MyTaggerTagsMytagged(o2o_tagging.O2OTag):
        tagger = 'myapp.Friend'
        tagged = 'myotherapp.Picture'
    ...

3. Tag your objects::

    ...
    tag = MyTaggerTagsMyTagged.objects.tag(tagger=tagger, tagged=tagged)
    ...

Running the Tests
-----------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py
