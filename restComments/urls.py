__author__ = 'Aston'

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('restComments.views',
    url(r'^comments/$', 'comment_list'),
    #url(r'^comments/(?P<pk>[0-9]+)$', 'comment_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)