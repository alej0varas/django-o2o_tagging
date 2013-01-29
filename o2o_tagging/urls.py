from django.conf.urls.defaults import patterns, url

from .views import TagCreateView


urlpatterns = patterns('',
    url('^tag/create/$', TagCreateView.as_view(), name='o2o_taggin_tag_create'),
)
