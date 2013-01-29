import django.dispatch

o2o_tag_created = django.dispatch.Signal(providing_args=["instance", ])
