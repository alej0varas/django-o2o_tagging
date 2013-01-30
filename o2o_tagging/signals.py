import django.dispatch

o2o_tag_created = django.dispatch.Signal(providing_args=["instance", ])
o2o_tags_created = django.dispatch.Signal(providing_args=["instances", ])
