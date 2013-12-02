__author__ = 'Aston'

from django.conf.urls import patterns, url

urlpatterns = patterns('jqmFlatPages.views',
    #url(r'^flat/$', 'page_list'),
    url(r'^flat/(?P<pk>\d+)/$', 'page_detail'),
    url(r'^flat/(?P<pid>[^/]+)/$', 'page_for_id'),
)
